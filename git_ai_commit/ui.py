"""Terminal UI for git-ai-commit."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

from .models import CommitMessage, CommitType

custom_theme = Theme(
    {
        "info": "cyan",
        "success": "bold green",
        "warning": "bold yellow",
        "error": "bold red",
        "type.feat": "bold green",
        "type.fix": "bold red",
        "type.refactor": "bold blue",
        "type.docs": "bold cyan",
        "type.chore": "dim white",
        "type.perf": "bold yellow",
        "type.test": "bold magenta",
        "type.style": "bold white",
        "type.ci": "dim cyan",
        "type.build": "dim yellow",
    }
)

console = Console(theme=custom_theme)


def print_banner() -> None:
    """Print the application banner."""
    banner = Text()
    banner.append("  ╔══════════════════════════════════════╗\n", style="bold cyan")
    banner.append("  ║   ", style="bold cyan")
    banner.append("🤖 git-ai-commit", style="bold white")
    banner.append("                    ║\n", style="bold cyan")
    banner.append("  ║   ", style="bold cyan")
    banner.append("AI-powered commit messages", style="dim white")
    banner.append("         ║\n", style="bold cyan")
    banner.append("  ╚══════════════════════════════════════╝", style="bold cyan")
    console.print(banner)
    console.print()


def print_no_staged() -> None:
    """Print message when no staged changes found."""
    console.print()
    console.print(
        Panel(
            "[warning]No staged changes found.[/warning]\n\n"
            "Stage some files first:\n"
            "  [dim]$ git add <files>[/dim]\n\n"
            "Then run [bold]git-ai-commit[/bold] again.",
            title="⚠️  Nothing to commit",
            border_style="yellow",
        )
    )


def print_diff_summary(files: list[str], stat: str) -> None:
    """Print a summary of staged changes."""
    table = Table(
        title="📋 Staged Changes",
        show_header=True,
        header_style="bold",
        border_style="dim",
        title_style="bold",
    )
    table.add_column("File", style="cyan", no_wrap=True)

    for f in files:
        table.add_row(f)

    console.print(table)
    console.print()


def print_generating(backend: str, model: str) -> None:
    """Print generating message."""
    console.print(
        f"  [dim]⏳ Generating with [bold]{backend}[/bold] ({model})...[/dim]"
    )


def print_commit_message(msg: CommitMessage, emoji: bool = False) -> None:
    """Print the generated commit message beautifully."""
    type_style = f"type.{msg.type.value}"

    header = msg.header
    if emoji:
        header = f"{msg.type.emoji} {header}"

    body_text = msg.body or ""

    content = Text()
    content.append(header, style="bold")
    if body_text:
        content.append("\n\n")
        content.append(body_text, style="dim")

    panel = Panel(
        content,
        title=f"{msg.type.emoji} Suggested Commit",
        subtitle=f"[dim]{msg.type.label}[/dim]",
        border_style=type_style.replace("type.", ""),
        padding=(1, 2),
    )
    console.print(panel)


def prompt_action() -> str:
    """Prompt user for action."""
    console.print()
    choices = {
        "a": "Accept & commit",
        "e": "Edit message",
        "r": "Regenerate",
        "q": "Quit",
    }

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Key", style="bold green")
    table.add_column("Action")

    for key, action in choices.items():
        table.add_row(f"[{key}]", action)

    console.print(table)
    console.print()

    return Prompt.ask(
        "Choose",
        choices=["a", "e", "r", "q"],
        default="a",
    )


def prompt_edit(current: CommitMessage) -> CommitMessage:
    """Let the user edit the commit message."""
    console.print()
    console.print("[dim]Edit the commit message (leave blank to keep current):[/dim]")
    console.print()

    new_subject = Prompt.ask("Subject", default=current.subject)
    new_body = Prompt.ask("Body", default=current.body or "")

    return CommitMessage(
        type=current.type,
        scope=current.scope,
        subject=new_subject,
        body=new_body or None,
        breaking=current.breaking,
        breaking_description=current.breaking_description,
    )


def print_success(message: str) -> None:
    """Print a success message."""
    console.print()
    console.print(f"  [success]✅ {message}[/success]")
    console.print()


def print_error(message: str) -> None:
    """Print an error message."""
    console.print()
    console.print(f"  [error]❌ {message}[/error]")
    console.print()
