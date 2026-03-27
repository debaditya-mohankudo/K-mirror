"""
Rich-based CLI interface for K-Mirror.

Provides a beautiful terminal UI for conversation with K-Mirror.
"""

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.prompt import Prompt
from rich.text import Text
from rich.rule import Rule

from app import create_app
from config import Settings


console = Console()


def welcome_screen():
    """Display welcome screen."""
    welcome_text = """
# K-Mirror: A Krishnamurti-Inspired Psychological Companion

> "Truth is a pathless land." — K. Krishnamurti

K-Mirror helps you explore psychological patterns through gentle inquiry.
Rather than giving answers, it asks questions that help you see clearly.

**How it works:**
- Share what's on your mind
- K-Mirror mirrors your words back through the lens of K's principles
- Explore patterns together
- Discover insight through direct observation

Type `/help` for commands.
"""
    console.print(Panel(welcome_text, title="Welcome", border_style="cyan"))


def help_screen():
    """Display help information."""
    help_text = """
**Commands:**
- `/new` - Start a new conversation
- `/sessions` - View previous sessions
- `/load <session_id>` - Load a previous session
- `/stats` - Show conversation statistics
- `/rag` - Show RAG store stats
- `/end` - End conversation and save
- `/help` - Show this help
- `/quit` or `Ctrl+C` - Exit

**Tips:**
- Be honest and specific about what you're experiencing
- Notice patterns across your responses
- Direct observation matters more than intellectual understanding
- Take your time; there's no rush
"""
    console.print(Panel(help_text, title="Help", border_style="cyan"))


def main():
    """Main CLI entry point."""
    try:
        # Initialize app
        settings = Settings()
        app = create_app(settings)

        console.print("\n")
        welcome_screen()
        console.print("\n")

        # Start new session
        session = app.new_session()
        console.print(f"[cyan]Session ID: {session.session_id}[/cyan]\n")

        # Conversation loop
        while True:
            try:
                user_input = Prompt.ask("[bold green]You[/bold green]")

                # Handle commands
                if user_input.startswith("/"):
                    handle_command(user_input, app)
                    continue

                # Process input
                console.print("[yellow]K-Mirror is thinking...[/yellow]")
                response = app.process_input(user_input)

                # Display response
                console.print(Panel(response, title="[bold blue]K-Mirror[/bold blue]", border_style="blue"))
                console.print()

            except KeyboardInterrupt:
                console.print("\n[yellow]Exiting... (use /quit to save session)[/yellow]")
                break

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()


def handle_command(command: str, app):
    """Handle CLI commands."""
    cmd = command.lower().strip()

    if cmd == "/help":
        help_screen()

    elif cmd == "/new":
        session = app.new_session()
        console.print(f"[green]New session started: {session.session_id}[/green]\n")

    elif cmd == "/sessions":
        sessions = app.get_sessions()
        if not sessions:
            console.print("[yellow]No previous sessions found[/yellow]\n")
            return

        table = Table(title="Previous Sessions")
        table.add_column("Session ID", style="cyan")
        table.add_column("Created", style="magenta")
        table.add_column("Turns", style="yellow")

        for session in sessions[:10]:  # Show last 10
            table.add_row(
                session["session_id"][:8] + "...",
                session["created_at"][:10],
                str(session["turns"])
            )

        console.print(table)
        console.print()

    elif cmd.startswith("/load"):
        parts = cmd.split()
        if len(parts) < 2:
            console.print("[red]Usage: /load <session_id>[/red]\n")
            return

        session_id = parts[1]
        session = app.load_session(session_id)
        if session:
            console.print(f"[green]Session loaded: {session.session_id}[/green]\n")
        else:
            console.print(f"[red]Session not found: {session_id}[/red]\n")

    elif cmd == "/stats":
        if app.current_session:
            state = app.current_session.state
            table = Table(title="Conversation Statistics")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="yellow")

            table.add_row("Turn", str(state.turn_number))
            table.add_row("Depth Level", f"{state.depth_level}/3")
            table.add_row("Patterns", ", ".join([p.value for p in state.current_patterns]) or "None")
            table.add_row("Principles", ", ".join([str(p) for p in state.matched_principles]) or "None")

            console.print(table)
            console.print()
        else:
            console.print("[yellow]No active session[/yellow]\n")

    elif cmd == "/rag":
        stats = app.get_rag_stats()
        table = Table(title="RAG Store Statistics")
        table.add_column("Collection", style="cyan")
        table.add_column("Count", style="yellow")

        for key, value in stats.items():
            table.add_row(key.replace("_", " ").title(), str(value))

        console.print(table)
        console.print()

    elif cmd == "/end":
        summary = app.end_conversation()
        console.print(Panel(
            f"""Session ended.

**Summary:**
- Duration: {summary.get('duration', 0):.0f} seconds
- Turns: {summary.get('turns', 0)}
- Depth reached: {summary.get('depth_reached', 0)}/3
- Patterns explored: {len(summary.get('patterns_explored', []))}

Session saved for future reference.
""",
            title="[bold green]Session Complete[/bold green]",
            border_style="green"
        ))
        console.print()

    elif cmd == "/quit":
        summary = app.end_conversation()
        console.print(Panel(
            "Session saved. Goodbye!",
            border_style="cyan"
        ))
        exit(0)

    else:
        console.print(f"[yellow]Unknown command: {cmd}. Type /help for commands.[/yellow]\n")


if __name__ == "__main__":
    main()
