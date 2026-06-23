"""Tests for git-ai-commit AI backends."""

import json

import pytest

from git_ai_commit.ai_backends import _parse_commit_json
from git_ai_commit.models import CommitType


class TestParseCommitJson:
    def test_parse_simple(self):
        raw = (
            '{"type": "feat", "scope": null, "subject": "add auth", '
            '"body": null, "breaking": false, "breaking_description": null}'
        )
        msg = _parse_commit_json(raw)
        assert msg.type == CommitType.FEAT
        assert msg.scope is None
        assert msg.subject == "add auth"
        assert msg.body is None

    def test_parse_with_body(self):
        raw = json.dumps({
            "type": "fix",
            "scope": "api",
            "subject": "handle timeout",
            "body": "Added retry logic with exponential backoff",
            "breaking": False,
            "breaking_description": None,
        })
        msg = _parse_commit_json(raw)
        assert msg.type == CommitType.FIX
        assert msg.scope == "api"
        assert msg.body == "Added retry logic with exponential backoff"

    def test_parse_with_extra_text(self):
        raw = (
            'Here is the commit message:\n'
            '{"type": "chore", "scope": null, "subject": "update deps", '
            '"body": null, "breaking": false, "breaking_description": null}'
            '\nDone.'
        )
        msg = _parse_commit_json(raw)
        assert msg.type == CommitType.CHORE
        assert msg.subject == "update deps"

    def test_parse_invalid_json(self):
        with pytest.raises(ValueError, match="Could not parse"):
            _parse_commit_json("not json at all")

    def test_parse_breaking_change(self):
        raw = json.dumps({
            "type": "feat",
            "scope": "api",
            "subject": "new response format",
            "body": "Changed response structure",
            "breaking": True,
            "breaking_description": "Response no longer includes 'data' wrapper",
        })
        msg = _parse_commit_json(raw)
        assert msg.breaking is True
        assert "data" in (msg.breaking_description or "")
        assert "!" in msg.header
