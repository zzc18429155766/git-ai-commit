"""Tests for git-ai-commit models."""

from git_ai_commit.models import Backend, CommitMessage, CommitType, Config


class TestCommitType:
    def test_emoji(self):
        assert CommitType.FEAT.emoji == "✨"
        assert CommitType.FIX.emoji == "🐛"
        assert CommitType.DOCS.emoji == "📚"

    def test_label(self):
        assert CommitType.FEAT.label == "Feature"
        assert CommitType.FIX.label == "Bug Fix"


class TestCommitMessage:
    def test_header_simple(self):
        msg = CommitMessage(type=CommitType.FEAT, scope=None, subject="add login page")
        assert msg.header == "feat: add login page"

    def test_header_with_scope(self):
        msg = CommitMessage(type=CommitType.FIX, scope="auth", subject="handle null token")
        assert msg.header == "fix(auth): handle null token"

    def test_header_breaking(self):
        msg = CommitMessage(
            type=CommitType.FEAT,
            scope="api",
            subject="change response format",
            breaking=True,
        )
        assert msg.header == "feat(api)!: change response format"

    def test_format_full(self):
        msg = CommitMessage(
            type=CommitType.FEAT,
            scope=None,
            subject="add feature",
            body="This adds the new feature\nwith detailed explanation.",
        )
        result = msg.format()
        assert "feat: add feature" in result
        assert "This adds the new feature" in result

    def test_format_no_body(self):
        msg = CommitMessage(
            type=CommitType.FEAT,
            scope=None,
            subject="add feature",
            body="Some body",
        )
        result = msg.format(include_body=False)
        assert "Some body" not in result

    def test_str(self):
        msg = CommitMessage(type=CommitType.CHORE, scope=None, subject="update deps")
        assert str(msg) == "chore: update deps"


class TestConfig:
    def test_defaults(self):
        config = Config()
        assert config.backend == Backend.OPENAI
        assert config.auto_commit is False
        assert config.max_subject_length == 72

    def test_default_model_openai(self):
        config = Config(backend=Backend.OPENAI)
        assert config.default_model == "gpt-4o"

    def test_default_model_anthropic(self):
        config = Config(backend=Backend.ANTHROPIC)
        assert config.default_model == "claude-sonnet-4-20250514"

    def test_default_model_ollama(self):
        config = Config(backend=Backend.OLLAMA)
        assert config.default_model == "llama3.1"

    def test_custom_model(self):
        config = Config(model="gpt-3.5-turbo")
        assert config.default_model == "gpt-3.5-turbo"
