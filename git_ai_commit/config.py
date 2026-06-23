"""Configuration loading for git-ai-commit."""

from __future__ import annotations

import os
from pathlib import Path

import yaml

from .models import Backend, Config


DEFAULT_CONFIG_FILENAMES = [".git-ai-commit.yml", ".git-ai-commit.yaml"]


def find_config_file() -> Path | None:
    """Find config file in current directory or git root."""
    cwd = Path.cwd()
    for name in DEFAULT_CONFIG_FILENAMES:
        p = cwd / name
        if p.exists():
            return p

    # Try git root
    try:
        import subprocess

        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
        root = Path(result.stdout.strip())
        for name in DEFAULT_CONFIG_FILENAMES:
            p = root / name
            if p.exists():
                return p
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # Try home directory
    home = Path.home()
    for name in DEFAULT_CONFIG_FILENAMES:
        p = home / name
        if p.exists():
            return p

    return None


def load_config() -> Config:
    """Load configuration from file and environment."""
    config = Config()

    config_file = find_config_file()
    if config_file:
        with open(config_file) as f:
            data = yaml.safe_load(f) or {}

        if "backend" in data:
            config.backend = Backend(data["backend"])
        if "model" in data:
            config.model = data["model"]
        if "auto_commit" in data:
            config.auto_commit = data["auto_commit"]
        if "include_body" in data:
            config.include_body = data["include_body"]
        if "max_subject_length" in data:
            config.max_subject_length = data["max_subject_length"]
        if "temperature" in data:
            config.temperature = data["temperature"]
        if "language" in data:
            config.language = data["language"]
        if "emoji" in data:
            config.emoji = data["emoji"]
        if "signoff" in data:
            config.signoff = data["signoff"]
        if "allowed_types" in data:
            config.allowed_types = data["allowed_types"]

    # Environment overrides
    env_backend = os.environ.get("GAC_BACKEND")
    if env_backend:
        config.backend = Backend(env_backend)

    env_model = os.environ.get("GAC_MODEL")
    if env_model:
        config.model = env_model

    return config
