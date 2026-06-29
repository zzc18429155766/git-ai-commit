"""Data models for git-ai-commit."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class CommitType(str, Enum):
    """Conventional commit types."""

    FEAT = "feat"
    FIX = "fix"
    REFACTOR = "refactor"
    DOCS = "docs"
    CHORE = "chore"
    PERF = "perf"
    TEST = "test"
    STYLE = "style"
    CI = "ci"
    BUILD = "build"

    @property
    def emoji(self) -> str:
        """Return emoji for commit type."""
        mapping = {
            "feat": "✨",
            "fix": "🐛",
            "refactor": "♻️",
            "docs": "📚",
            "chore": "🔧",
            "perf": "⚡",
            "test": "🧪",
            "style": "💎",
            "ci": "🤖",
            "build": "📦",
        }
        return mapping.get(self.value, "📝")

    @property
    def label(self) -> str:
        """Return human-readable label."""
        mapping = {
            "feat": "Feature",
            "fix": "Bug Fix",
            "refactor": "Refactor",
            "docs": "Documentation",
            "chore": "Chore",
            "perf": "Performance",
            "test": "Test",
            "style": "Style",
            "ci": "CI",
            "build": "Build",
        }
        return mapping.get(self.value, "Other")


class Backend(str, Enum):
    """Supported AI backends."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"


@dataclass
class CommitMessage:
    """A generated commit message."""

    type: CommitType
    scope: str | None
    subject: str
    body: str | None = None
    breaking: bool = False
    breaking_description: str | None = None

    @property
    def header(self) -> str:
        """Generate the commit header line."""
        prefix = f"{self.type.value}"
        if self.scope:
            prefix += f"({self.scope})"
        if self.breaking:
            prefix += "!"
        return f"{prefix}: {self.subject}"

    def format(self, include_body: bool = True) -> str:
        """Format the full commit message."""
        parts = [self.header]
        if include_body and self.body:
            parts.append("")
            parts.append(self.body)
        if self.breaking and self.breaking_description:
            parts.append("")
            parts.append(f"BREAKING CHANGE: {self.breaking_description}")
        return "\n".join(parts)

    def __str__(self) -> str:
        return self.format()


@dataclass
class Config:
    """Configuration for git-ai-commit."""

    backend: Backend = Backend.OPENAI
    model: str | None = None
    auto_commit: bool = False
    include_body: bool = True
    max_subject_length: int = 72
    temperature: float = 0.3
    language: str = "en"
    emoji: bool = False
    signoff: bool = False
    allowed_types: list[str] = field(default_factory=lambda: [t.value for t in CommitType])

    @property
    def default_model(self) -> str:
        """Return the default model for the configured backend."""
        if self.model:
            return self.model
        defaults = {
            Backend.OPENAI: "gpt-4o",
            Backend.ANTHROPIC: "claude-sonnet-4-20250514",
            Backend.OLLAMA: "llama3.1",
        }
        return defaults.get(self.backend, "gpt-4o")
