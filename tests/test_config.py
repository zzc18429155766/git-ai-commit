"""Tests for git-ai-commit config loading."""

import yaml

from git_ai_commit.config import load_config
from git_ai_commit.models import Backend


def test_load_config_defaults(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    config = load_config()
    assert config.backend == Backend.OPENAI
    assert config.auto_commit is False


def test_load_config_from_file(tmp_path, monkeypatch):
    cfg = {
        "backend": "ollama",
        "model": "mistral",
        "auto_commit": True,
        "emoji": True,
        "language": "zh",
    }
    cfg_file = tmp_path / ".git-ai-commit.yml"
    cfg_file.write_text(yaml.dump(cfg))
    monkeypatch.chdir(tmp_path)

    config = load_config()
    assert config.backend == Backend.OLLAMA
    assert config.model == "mistral"
    assert config.auto_commit is True
    assert config.emoji is True
    assert config.language == "zh"


def test_load_config_env_override(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GAC_BACKEND", "anthropic")
    monkeypatch.setenv("GAC_MODEL", "claude-3-opus-20240229")

    config = load_config()
    assert config.backend == Backend.ANTHROPIC
    assert config.model == "claude-3-opus-20240229"
