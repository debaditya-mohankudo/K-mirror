"""
K-Mirror main application.

Orchestrates the LangGraph pipeline with all 5 nodes.
"""

from typing import Optional
from langgraph.graph import StateGraph, START, END
from langchain_anthropic import ChatAnthropic

from state import KMirrorState
from principles import PRINCIPLES
from nodes_simplified import (
    listener_node,
    classifier_node,
    retriever_node,
    depth_assessor_node
)
from rag import RAGStore
from session import Session, SessionManager
from config import Settings


class KMirrorApp:
    """Main K-Mirror application orchestrator."""

    def __init__(self, settings: Optional[Settings] = None):
        """
        Initialize K-Mirror app.

        Args:
            settings: Configuration (uses defaults if not provided)
        """
        self.settings = settings or Settings()
        self.client = ChatAnthropic(model="claude-3-5-sonnet-20241022")
        self.rag_store = RAGStore(self.settings)
        self.session_manager = SessionManager()
        self.current_session: "Optional[Session]" = None

        # Build the graph
        self.graph = self._build_graph()
        self.compiled_graph = self.graph.compile()

    def _build_graph(self):
        """Build the LangGraph state machine (analysis only, no LLM)."""
        graph = StateGraph(KMirrorState)

        # Add all nodes (analysis only, no LLM calls)
        graph.add_node("listener", listener_node)
        graph.add_node("classifier", classifier_node)

        # Retriever node with RAG store
        def retriever_wrapper(state):
            return retriever_node(state, self.rag_store)

        graph.add_node("retriever", retriever_wrapper)
        graph.add_node("depth_assessor", depth_assessor_node)

        # Wire the edges (no inquiry generator since no LLM)
        graph.add_edge(START, "listener")
        graph.add_edge("listener", "classifier")
        graph.add_edge("classifier", "retriever")
        graph.add_edge("retriever", "depth_assessor")
        graph.add_edge("depth_assessor", END)

        return graph

    def new_session(self) -> Session:
        """Start a new conversation session."""
        session = self.session_manager.create_session()
        self.current_session = session
        return session

    def analyze_input(self, user_input: str, session: Optional[Session] = None) -> dict:
        """
        Analyze user input without generating LLM response.

        Returns context that Claude can use to generate a response.

        Args:
            user_input: User's message
            session: Optional session (uses current if not provided)

        Returns:
            Dict with analysis:
            - patterns: List[PsychPattern]
            - principles: List[int] (principle IDs)
            - passages: List[str] (K passages)
            - dialogue_approaches: List[str]
            - depth_level: int (0-3)
            - key_phrases: List[str]
            - context_words: List[str]
            - emotional_tone: str
            - resistance_signals: List[str]
        """
        if session is None:
            if not self.current_session:
                self.new_session()
            session = self.current_session

        # Create temporary state for analysis
        from langchain_core.messages import HumanMessage

        # Get current turn number from session
        current_turn = 1
        if hasattr(session, 'state') and hasattr(session.state, 'turn_number'):
            current_turn = session.state.turn_number + 1

        state = KMirrorState(
            messages=[HumanMessage(content=user_input)],
            session_id=session.session_id,
            turn_number=current_turn
        )

        # Run through analysis pipeline (no LLM)
        output_state = self.compiled_graph.invoke(state)

        # Handle both dict and object responses
        if isinstance(output_state, dict):
            matched = output_state.get('matched_principles', [])
            patterns = output_state.get('current_patterns', [])
            passages = output_state.get('retrieved_passages', [])
            depth = output_state.get('depth_level', 0)
            phrases = output_state.get('key_phrases', [])
            context = output_state.get('context_words', [])
            tone = output_state.get('emotional_tone', 'neutral')
            resistance = output_state.get('resistance_signals', [])
        else:
            matched = output_state.matched_principles
            patterns = output_state.current_patterns
            passages = output_state.retrieved_passages
            depth = output_state.depth_level
            phrases = output_state.key_phrases
            context = output_state.context_words
            tone = output_state.emotional_tone
            resistance = output_state.resistance_signals

        # Get related principles and approaches
        approaches = []
        for principle_id in matched[:2]:
            if principle_id in PRINCIPLES:
                approaches.extend(PRINCIPLES[principle_id].dialogue_approaches)
        approaches = list(set(approaches))[:3]  # Unique, max 3

        return {
            "patterns": patterns,
            "principles": matched,
            "passages": passages,
            "dialogue_approaches": approaches,
            "depth_level": depth,
            "key_phrases": phrases,
            "context_words": context,
            "emotional_tone": tone,
            "resistance_signals": resistance,
        }

    def load_session(self, session_id: str) -> Optional[Session]:
        """Load a previous session."""
        session = self.session_manager.load_session(session_id)
        if session:
            self.current_session = session
        return session

    def process_input(self, user_input: str) -> dict:
        """
        Process user input and return analysis for Claude to use.

        Now returns analysis instead of generating response.
        Claude Code handles dialogue generation using this analysis.

        Args:
            user_input: User's message

        Returns:
            Dict with analysis context for Claude
        """
        if not self.current_session:
            self.new_session()

        session = self.current_session
        session.add_message(user_input, role="user")

        # Get analysis
        analysis = self.analyze_input(user_input, session)

        return analysis

    def save_response(self, response_text: str, principle_id: int, outcome: str = "unknown"):
        """
        Save Claude's response to the database.

        Call this after Claude generates a response.

        Args:
            response_text: The response Claude generated
            principle_id: ID of the principle used
            outcome: "explored", "deflected", "seen", "surface", or "unknown"
        """
        if self.current_session:
            self.current_session.save_question(response_text, principle_id, outcome)

    def end_conversation(self) -> dict:
        """End the current session and return summary."""
        if not self.current_session:
            return {}

        summary = self.current_session.end_session()
        self.session_manager.save_session(self.current_session)
        return summary

    def get_sessions(self) -> list:
        """List all saved sessions."""
        return self.session_manager.list_sessions()

    def get_rag_stats(self) -> dict:
        """Get statistics about the RAG store."""
        return self.rag_store.get_stats()


# Convenience function
def create_app(settings: Optional[Settings] = None) -> KMirrorApp:
    """Factory function to create a K-Mirror app instance."""
    return KMirrorApp(settings)
