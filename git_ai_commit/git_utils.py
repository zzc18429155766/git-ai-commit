"""Git operations for git-ai-commit."""

from __future__ import annotations

import subprocess
import sys


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    """Run a git command and return the result."""
    cmd = ["git", *args]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=check,
        )
        return result
    except FileNotFoundError:
        print("Error: git is not installed or not in PATH", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        if check:
            print(f"Error running git: {e.stderr.strip()}", file=sys.stderr)
            sys.exit(1)
        return e


def is_git_repo() -> bool:
    """Check if current directory is a git repository."""
    result = run_git("rev-parse", "--is-inside-work-tree", check=False)
    return result.returncode == 0


def get_staged_diff() -> str:
    """Get the staged diff."""
    result = run_git("diff", "--staged")
    return result.stdout


def get_staged_files() -> list[str]:
    """Get list of staged files."""
    result = run_git("diff", "--cached", "--name-only")
    return [f for f in result.stdout.strip().split("\n") if f]


def get_staged_stat() -> str:
    """Get staged diff --stat."""
    result = run_git("diff", "--cached", "--stat")
    return result.stdout.strip()


def get_branch_name() -> str:
    """Get current branch name."""
    result = run_git("rev-parse", "--abbrev-ref", "HEAD", check=False)
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def commit(message: str, signoff: bool = False, amend: bool = False) -> None:
    """Create a git commit with the given message."""
    args = ["commit", "-m", message]
    if signoff:
        args.append("-s")
    if amend:
        args.append("--amend")
    run_git(*args)
