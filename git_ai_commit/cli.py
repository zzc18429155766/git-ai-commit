"""CLI entry point for git-ai-commit."""

from __future__ import annotations

import sys

import click

from . import __version__
from .ai_backends import get_backend
from .config import load_config
from .git_utils import commit, get_branch_name, get_staged_diff, get_staged_files, get_staged_stat, is_git_repo
from .models import Backend, CommitMessage, Config
from .ui import (
    console,
    print_banner,
    print_commit_message,
    print_diff_summary,
    print_error,
    print_generating,
    print_no_staged,
    print_success,
    prompt_action,
    prompt_edit,
)


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=__version__, prog_name="git-ai-commit")
@click.option(
    "-b",
    "--backend",
    type=click.Choice(["openai", "anthropic", "ollama"], case_sensitive=False),
    help="AI backend to use",
)
@click.option("-m", "--model", help="Model to use (e.g. gpt-4o, claude-sonnet-4-20250514)")
@click.option("-a", "--auto", is_flag=True, help="Auto-commit without prompting")
@click.option("--no-body", is_flag=True, help="Skip generating commit body")
@click.option("--emoji", is_flag=True, help="Add emoji prefix to commit message")
@click.option("--signoff", is_flag=True, help="Add Signed-off-by trailer")
@click.option("--dry-run", is_flag=True, help="Show message without committing")
@click.option("--amend", is_flag=True, help="Amend the last commit")
@click.option(
    "-l", "--language", help="Language for commit message (e.g. en, zh, ja)"
)
@click.option("-v", "--verbose", is_flag=True, help="Show detailed output")
def main(
    backend: str | None,
    model: str | None,
    auto: bool,
    no_body: bool,
    emoji: bool,
    signoff: bool,
    dry_run: bool,
    amend: bool,
    language: str | None,
    verbose: bool,
) -> None:
    """Generate beautiful commit messages from staged diffs using AI.

    Works as a standalone CLI or as a git subcommand:
      $ git ai-commit
      $ git-ai-commit

    \b
    Examples:
      git-ai-commit                    # Interactive mode
      git-ai-commit --auto             # Auto-commit
      git-ai-commit --backend ollama   # Use local Ollama
      git-ai-commit --dry-run          # Preview only
    """
    # Check git repo
    if not is_git_repo():
        print_error("Not a git repository. Run this from inside a git repo.")
        sys.exit(1)

    # Load config
    config = load_config()

    # CLI overrides
    if backend:
        config.backend = Backend(backend)
    if model:
        config.model = model
    if auto:
        config.auto_commit = True
    if no_body:
        config.include_body = False
    if emoji:
        config.emoji = True
    if signoff:
        config.signoff = True
    if language:
        config.language = language

    # Banner
    if not dry_run or verbose:
        print_banner()

    # Get staged changes
    diff = get_staged_diff()
    if not diff.strip():
        print_no_staged()
        sys.exit(0)

    files = get_staged_files()
    stat = get_staged_stat()

    # Show diff summary
    print_diff_summary(files, stat)

    # Generate commit message
    ai_backend = get_backend(config.backend)

    ai_config = {
        "model": config.default_model,
        "temperature": config.temperature,
        "max_subject_length": config.max_subject_length,
        "allowed_types": config.allowed_types,
        "language": config.language,
        "emoji": config.emoji,
        "files": ", ".join(files),
    }

    # Add API keys from environment
    import os
    ai_config["api_key"] = os.environ.get(
        f"{config.backend.value.upper()}_API_KEY", ""
    )

    print_generating(config.backend.value, config.default_model)

    try:
        msg = ai_backend.generate(diff, ai_config)
    except Exception as e:
        print_error(f"Failed to generate commit message: {e}")
        sys.exit(1)

    # Display and interact
    if config.auto_commit:
        print_commit_message(msg, emoji=config.emoji)
        if dry_run:
            console.print("[dim](dry run — not committing)[/dim]")
        else:
            final = msg.format(include_body=config.include_body)
            commit(final, signoff=config.signoff, amend=amend)
            print_success("Committed successfully!")
        return

    # Interactive mode
    while True:
        print_commit_message(msg, emoji=config.emoji)
        action = prompt_action()

        if action == "a":
            if dry_run:
                console.print("\n[dim](dry run — not committing)[/dim]")
                console.print("\n[dim]Message would be:[/dim]")
                console.print(msg.format(include_body=config.include_body))
                break

            final_msg = msg.format(include_body=config.include_body)
            try:
                commit(final_msg, signoff=config.signoff, amend=amend)
                print_success("Committed successfully!")
            except SystemExit:
                print_error("Commit failed.")
                sys.exit(1)
            break

        elif action == "e":
            msg = prompt_edit(msg)
            # Re-render
            console.clear()

        elif action == "r":
            console.print("\n  [dim]🔄 Regenerating...[/dim]")
            try:
                msg = ai_backend.generate(diff, ai_config)
            except Exception as e:
                print_error(f"Failed to regenerate: {e}")
                sys.exit(1)

        elif action == "q":
            console.print("\n  [dim]Cancelled.[/dim]")
            break


if __name__ == "__main__":
    main()
