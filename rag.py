"""
RAG (Retrieval-Augmented Generation) integration using ChromaDB.

Manages the vector store for Krishnamurti passages and principles.
"""

from typing import List, Optional
import chromadb
from pathlib import Path

from config import Settings
from principles import PRINCIPLES


class RAGStore:
    """Vector store for K passages and principles."""

    def __init__(self, settings: Settings):
        """Initialize ChromaDB store."""
        self.settings = settings
        self.persist_dir = Path(settings.chroma_persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=str(self.persist_dir))

        # Get or create collections
        try:
            self.principles_collection = self.client.get_collection("principles")
        except:
            self.principles_collection = self.client.create_collection("principles")

        try:
            self.passages_collection = self.client.get_collection("passages")
        except:
            self.passages_collection = self.client.create_collection("passages")

        try:
            self.dialogue_patterns_collection = self.client.get_collection("dialogue_patterns")
        except:
            self.dialogue_patterns_collection = self.client.create_collection("dialogue_patterns")

        # Initialize with seed data if empty
        self._init_principles()
        self._init_seed_passages()

    def _init_principles(self):
        """Initialize principles collection with 12 K principles."""
        if self.principles_collection.count() > 0:
            return  # Already initialized

        for principle_id, principle in PRINCIPLES.items():
            text = f"{principle.name}: {principle.essence}"
            self.principles_collection.add(
                ids=[f"principle_{principle_id}"],
                documents=[text],
                metadatas=[{
                    "principle_id": principle_id,
                    "principle_name": principle.name,
                    "type": "principle"
                }]
            )

    def _init_seed_passages(self):
        """Initialize with seed passages from Krishnamurti teachings."""
        if self.passages_collection.count() > 0:
            return  # Already initialized

        seed_passages = [
            {
                "id": "passage_1",
                "text": "Can you observe your anger without naming it? When you name it, you separate yourself from it. The observer becomes different from the observed.",
                "principle": 1,
                "source": "Krishnamurti Talk"
            },
            {
                "id": "passage_2",
                "text": "Mechanical life—going to the office, routine, habit—gives a sense of security. But this mechanical movement is death. You are not living; you are merely existing.",
                "principle": 2,
                "source": "Krishnamurti Talk"
            },
            {
                "id": "passage_3",
                "text": "The self is the root of all problems. The self is what divides, what fragments. Without understanding the self, all action creates more disorder.",
                "principle": 3,
                "source": "Krishnamurti Talk"
            },
            {
                "id": "passage_4",
                "text": "Thought is material in nature. It is energy. When you have a thought about something, that thought is material. You can observe it, watch it arise and pass.",
                "principle": 4,
                "source": "Krishnamurti Talk"
            },
            {
                "id": "passage_5",
                "text": "Real action has no choice in it. When there is choice, there is fragmentation, conflict. But when you move from direct seeing, there is no chooser.",
                "principle": 5,
                "source": "Krishnamurti Talk"
            },
            {
                "id": "passage_6",
                "text": "Can thought come to stillness on its own? Or does stillness come only when thought is no longer seeking? What is the nature of silence when there is no seeking?",
                "principle": 6,
                "source": "Krishnamurti Talk"
            },
            {
                "id": "passage_7",
                "text": "In relationship, we carry images of each other. These images are dead; they kill relationship. When you meet someone with an image, you are not meeting them at all.",
                "principle": 7,
                "source": "Krishnamurti Talk"
            },
            {
                "id": "passage_8",
                "text": "Fear is the movement of thought in time. You are afraid of the future because thought has created a continuity between now and tomorrow. Can you see this movement?",
                "principle": 8,
                "source": "Krishnamurti Talk"
            },
            {
                "id": "passage_9",
                "text": "Comparison is the root of violence—violence against yourself, against others. When you compare, there is always a fragment that feels less. This fragmentation is violence.",
                "principle": 9,
                "source": "Krishnamurti Talk"
            },
            {
                "id": "passage_10",
                "text": "Freedom is not from something. Freedom is the act of seeing clearly. When you see the trap you are in, you are already out of it.",
                "principle": 10,
                "source": "Krishnamurti Talk"
            },
            {
                "id": "passage_11",
                "text": "The word is not the thing. When you say 'I am depressed,' you have named the state with a word. But the naming is not the fact. What is actually happening without the word?",
                "principle": 11,
                "source": "Krishnamurti Talk"
            },
            {
                "id": "passage_12",
                "text": "Understanding requires no time. Understanding is immediate or it is not at all. Psychological time is the movement of the self avoiding the present.",
                "principle": 12,
                "source": "Krishnamurti Talk"
            },
        ]

        for passage in seed_passages:
            self.passages_collection.add(
                ids=[passage["id"]],
                documents=[passage["text"]],
                metadatas=[{
                    "principle_id": passage["principle"],
                    "source": passage["source"],
                    "type": "passage"
                }]
            )

    def query(self, query_text: str, top_k: int = 2) -> List[str]:
        """
        Query the RAG store for relevant passages.

        Args:
            query_text: Search query (principle name or user input)
            top_k: Number of top results to return

        Returns:
            List of relevant passages
        """
        try:
            # Search in both passages and principles
            passages_results = self.passages_collection.query(
                query_texts=[query_text],
                n_results=top_k
            )

            results = []
            if passages_results and passages_results['documents']:
                results.extend(passages_results['documents'][0])

            return results[:top_k]
        except Exception as e:
            print(f"RAG query error: {e}")
            return []

    def add_passage(
        self,
        text: str,
        principle_id: int,
        source: str = "User Added"
    ) -> None:
        """Add a new passage to the store."""
        passage_id = f"passage_{self.passages_collection.count() + 1}"
        self.passages_collection.add(
            ids=[passage_id],
            documents=[text],
            metadatas=[{
                "principle_id": principle_id,
                "source": source,
                "type": "passage"
            }]
        )

    def get_stats(self) -> dict:
        """Get statistics about the RAG store."""
        return {
            "principles_count": self.principles_collection.count(),
            "passages_count": self.passages_collection.count(),
            "dialogue_patterns_count": self.dialogue_patterns_collection.count(),
        }
