"""AI backend implementations for git-ai-commit."""

from __future__ import annotations

import json
import os
import re
import sys
from typing import Protocol

import httpx

from .models import Backend, CommitMessage, CommitType


class AIBackend(Protocol):
    """Protocol for AI backends."""

    def generate(self, diff: str, config: dict) -> CommitMessage: ...


SYSTEM_PROMPT = """You are an expert developer creating git commit messages.

Rules:
1. Use Conventional Commits format: type(scope): subject
2. Keep subject line under {max_subject_length} characters
3. Use imperative mood ("add" not "added")
4. Don't capitalize the first letter of the subject
5. No period at end of subject
6. Types: {allowed_types}
7. Detect the most appropriate type from the diff
8. Extract a concise scope if obvious (module, file group)
9. Generate a body explaining WHY, not just WHAT (if changes warrant it)
10. Detect breaking changes and mark with !

{language_instruction}
{emoji_instruction}

Respond ONLY with valid JSON in this exact format:
{{"type": "<type>", "scope": "<scope or null>",
"subject": "<subject>", "body": "<body or null>",
"breaking": false, "breaking_description": null}}
"""

USER_PROMPT = """Generate a commit message for this staged diff:

```diff
{diff}
```

Changed files: {files}
"""


def _build_system_prompt(
    max_subject_length: int,
    allowed_types: list[str],
    language: str,
    emoji: bool,
) -> str:
    lang_inst = ""
    if language != "en":
        lang_inst = f"Write the commit message body in {language}."

    emoji_inst = ""
    if emoji:
        emoji_inst = (
            "Prefix the subject with the appropriate gitmoji. "
            "Example: ✨ add user authentication"
        )

    return SYSTEM_PROMPT.format(
        max_subject_length=max_subject_length,
        allowed_types=", ".join(allowed_types),
        language_instruction=lang_inst,
        emoji_instruction=emoji_inst,
    )


def _parse_commit_json(raw: str) -> CommitMessage:
    """Parse the AI response JSON into a CommitMessage."""
    # Try to extract JSON from the response
    json_match = re.search(r"\{[^{}]*\}", raw, re.DOTALL)
    if not json_match:
        raise ValueError(f"Could not parse AI response as JSON:\n{raw}")

    data = json.loads(json_match.group())

    commit_type = CommitType(data.get("type", "chore"))
    return CommitMessage(
        type=commit_type,
        scope=data.get("scope"),
        subject=data.get("subject", ""),
        body=data.get("body"),
        breaking=data.get("breaking", False),
        breaking_description=data.get("breaking_description"),
    )


class OpenAIBackend:
    """OpenAI API backend."""

    def generate(self, diff: str, config: dict) -> CommitMessage:
        try:
            import openai
        except ImportError:
            print(
                "Error: openai package not installed. Install with: pip install 'git-ai-commit[openai]'",
                file=sys.stderr,
            )
            sys.exit(1)

        api_key = config.get("api_key") or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print(
                "Error: OPENAI_API_KEY not set. Set it via environment variable or config.",
                file=sys.stderr,
            )
            sys.exit(1)

        client = openai.OpenAI(api_key=api_key)
        system = _build_system_prompt(
            config["max_subject_length"],
            config["allowed_types"],
            config["language"],
            config["emoji"],
        )
        user = USER_PROMPT.format(diff=diff[:8000], files=config.get("files", ""))

        response = client.chat.completions.create(
            model=config.get("model", "gpt-4o"),
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=config.get("temperature", 0.3),
            max_tokens=500,
        )

        raw = response.choices[0].message.content or ""
        return _parse_commit_json(raw)


class AnthropicBackend:
    """Anthropic Claude API backend."""

    def generate(self, diff: str, config: dict) -> CommitMessage:
        try:
            import anthropic
        except ImportError:
            print(
                "Error: anthropic package not installed. Install with: pip install 'git-ai-commit[anthropic]'",
                file=sys.stderr,
            )
            sys.exit(1)

        api_key = config.get("api_key") or os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print(
                "Error: ANTHROPIC_API_KEY not set. Set it via environment variable or config.",
                file=sys.stderr,
            )
            sys.exit(1)

        client = anthropic.Anthropic(api_key=api_key)
        system = _build_system_prompt(
            config["max_subject_length"],
            config["allowed_types"],
            config["language"],
            config["emoji"],
        )
        user = USER_PROMPT.format(diff=diff[:8000], files=config.get("files", ""))

        response = client.messages.create(
            model=config.get("model", "claude-sonnet-4-20250514"),
            max_tokens=500,
            system=system,
            messages=[{"role": "user", "content": user}],
            temperature=config.get("temperature", 0.3),
        )

        raw = response.content[0].text
        return _parse_commit_json(raw)


class OllamaBackend:
    """Local Ollama API backend."""

    def generate(self, diff: str, config: dict) -> CommitMessage:
        base_url = config.get("ollama_url", "http://localhost:11434")
        model = config.get("model", "llama3.1")
        system = _build_system_prompt(
            config["max_subject_length"],
            config["allowed_types"],
            config["language"],
            config["emoji"],
        )
        user = USER_PROMPT.format(diff=diff[:8000], files=config.get("files", ""))

        try:
            resp = httpx.post(
                f"{base_url}/api/chat",
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                    "stream": False,
                    "options": {"temperature": config.get("temperature", 0.3)},
                },
                timeout=120,
            )
            resp.raise_for_status()
            data = resp.json()
            raw = data["message"]["content"]
        except httpx.ConnectError:
            print(
                f"Error: Could not connect to Ollama at {base_url}. "
                "Is Ollama running?",
                file=sys.stderr,
            )
            sys.exit(1)
        except httpx.HTTPStatusError as e:
            print(f"Error: Ollama API returned {e.response.status_code}", file=sys.stderr)
            sys.exit(1)

        return _parse_commit_json(raw)


BACKENDS: dict[Backend, type] = {
    Backend.OPENAI: OpenAIBackend,
    Backend.ANTHROPIC: AnthropicBackend,
    Backend.OLLAMA: OllamaBackend,
}


def get_backend(backend: Backend) -> AIBackend:
    """Get an instance of the specified backend."""
    cls = BACKENDS.get(backend)
    if cls is None:
        print(f"Error: Unknown backend '{backend}'", file=sys.stderr)
        sys.exit(1)
    return cls()  # type: ignore[return-value]
