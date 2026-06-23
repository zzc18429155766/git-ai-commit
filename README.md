<div align="center">

# 🤖 git-ai-commit

**Generate beautiful, conventional commit messages from your staged diffs using AI.**

[![PyPI version](https://img.shields.io/pypi/v/git-ai-commit?color=blue&logo=pypi&logoColor=white&style=for-the-badge)](https://pypi.org/project/git-ai-commit/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge&logo=opensourceinitiative)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![GitHub Stars](https://img.shields.io/github/stars/nousresearch/git-ai-commit?style=for-the-badge&logo=github)](https://github.com/nousresearch/git-ai-commit)
[![Downloads](https://img.shields.io/pypi/dm/git-ai-commit?style=for-the-badge&logo=pypi)](https://pypi.org/project/git-ai-commit/)

---

```
  ╔══════════════════════════════════════╗
  ║   🤖 git-ai-commit                  ║
  ║   AI-powered commit messages         ║
  ╚══════════════════════════════════════╝
```

[Installation](#installation) • [Quick Start](#quick-start) • [Features](#features) • [Configuration](#configuration) • [Backends](#backends) • [Contributing](#contributing)

</div>

---

## 📸 Demo

```
$ git add .
$ git-ai-commit

  ╔══════════════════════════════════════╗
  ║   🤖 git-ai-commit                  ║
  ║   AI-powered commit messages         ║
  ╚══════════════════════════════════════╝

          📋 Staged Changes
┌─────────────────────────────────────────┐
│ File                                    │
├─────────────────────────────────────────┤
│ src/auth/login.py                       │
│ src/auth/middleware.py                   │
│ tests/test_login.py                      │
└─────────────────────────────────────────┘

  ⏳ Generating with openai (gpt-4o)...

╭──────── ✨ Suggested Commit ────────╮
│                                      │
│  feat(auth): add JWT refresh token   │
│                                      │
│  Implement automatic token refresh   │
│  to prevent session expiry during    │
│  active user sessions.               │
│                                      │
╰──────────── Feature ────────────────╯

  [a] Accept & commit
  [e] Edit message
  [r] Regenerate
  [q] Quit

  Choose [a]:
  ✅ Committed successfully!
```

---

## 🚀 Installation

### pip (recommended)

```bash
pip install git-ai-commit
```

### With specific AI backend

```bash
# OpenAI
pip install "git-ai-commit[openai]"

# Anthropic
pip install "git-ai-commit[anthropic]"

# All backends
pip install "git-ai-commit[all]"
```

### pipx (isolated)

```bash
pipx install git-ai-commit
```

### Homebrew

```bash
brew install nousresearch/tap/git-ai-commit
```

### From source

```bash
git clone https://github.com/nousresearch/git-ai-commit.git
cd git-ai-commit
pip install -e ".[all]"
```

---

## ⚡ Quick Start

### 1. Set your API key

```bash
# OpenAI (default)
export OPENAI_API_KEY="sk-..."

# Or Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."

# Or use local Ollama (no key needed)
ollama pull llama3.1
```

### 2. Stage your changes and commit

```bash
git add .
git-ai-commit
```

That's it! 🎉

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎯 **Conventional Commits** | Automatically detects type (feat, fix, refactor, etc.) |
| 🧠 **Multi-AI Backend** | OpenAI, Anthropic, and local Ollama support |
| 💬 **Interactive Mode** | Accept, edit, or regenerate suggestions |
| ⚡ **Auto-commit** | One-step generate + commit |
| 📝 **Commit Body** | Generates detailed commit body explaining the *why* |
| 🎨 **Beautiful Output** | Rich terminal UI with colors and panels |
| ⚙️ **Configurable** | `.git-ai-commit.yml` config file support |
| 🌍 **Multi-language** | Generate messages in any language |
| 🔍 **Breaking Changes** | Detects and marks breaking changes with `!` |
| 🏷️ **Scopes** | Auto-detects scope from changed files |
| 📦 **Lightweight** | Minimal dependencies, fast startup |

---

## 📖 Usage

### Interactive Mode (default)

```bash
git-ai-commit
# or as git subcommand
git ai-commit
```

Shows a suggested commit message and lets you accept, edit, regenerate, or quit.

### Auto-commit Mode

```bash
git-ai-commit --auto
# or
git-ai-commit -a
```

Generates and commits in one step — perfect for rapid development.

### Dry Run

```bash
git-ai-commit --dry-run
```

Preview the generated message without committing.

### Choose Backend

```bash
git-ai-commit --backend openai
git-ai-commit --backend anthropic
git-ai-commit --backend ollama
```

### Specify Model

```bash
git-ai-commit --model gpt-4o-mini
git-ai-commit --model claude-sonnet-4-20250514
git-ai-commit --model codellama
```

### Add Emoji

```bash
git-ai-commit --emoji
```

Prefixes the subject with the appropriate gitmoji: `✨ feat: add login`

### Generate in Another Language

```bash
git-ai-commit --language zh   # Chinese
git-ai-commit --language ja   # Japanese
git-ai-commit --language es   # Spanish
```

### Sign-off

```bash
git-ai-commit --signoff
```

Adds `Signed-off-by` trailer to the commit.

### Amend Last Commit

```bash
git-ai-commit --amend
```

---

## ⚙️ Configuration

Create a `.git-ai-commit.yml` in your project root or home directory:

```yaml
# AI backend: openai | anthropic | ollama
backend: openai

# Model to use (optional — uses backend default)
model: gpt-4o

# Auto-commit without interactive prompt
auto_commit: false

# Generate commit message body
include_body: true

# Max subject line length
max_subject_length: 72

# Temperature (0.0 - 1.0) — lower = more deterministic
temperature: 0.3

# Language for commit messages
language: en

# Add emoji prefix
emoji: false

# Add Signed-off-by
signoff: false

# Restrict allowed commit types
allowed_types:
  - feat
  - fix
  - refactor
  - docs
  - chore
  - perf
  - test

# Ollama-specific: custom URL
ollama_url: http://localhost:11434
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key |
| `ANTHROPIC_API_KEY` | Anthropic API key |
| `GAC_BACKEND` | Override backend |
| `GAC_MODEL` | Override model |

---

## 🧠 Backends

### OpenAI

```bash
export OPENAI_API_KEY="sk-..."
git-ai-commit --backend openai --model gpt-4o
```

Default model: `gpt-4o`

### Anthropic

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
git-ai-commit --backend anthropic
```

Default model: `claude-sonnet-4-20250514`

### Ollama (local, free, private)

```bash
# 1. Install Ollama: https://ollama.ai
# 2. Pull a model
ollama pull llama3.1

# 3. Use it
git-ai-commit --backend ollama --model llama3.1
```

No API key required. Runs 100% locally. 🔒

---

## 🔧 Git Integration

### Git Alias

```bash
git config --global alias.ai '!git-ai-commit'
```

Then use:

```bash
git ai
git ai --auto
```

### Git Hook (pre-commit)

```bash
# .git/hooks/prepare-commit-msg
#!/bin/bash
if [ -z "$COMMIT_MSG_SOURCE" ]; then
    git-ai-commit --auto
fi
```

---

## 🧪 Development

```bash
# Clone
git clone https://github.com/nousresearch/git-ai-commit.git
cd git-ai-commit

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Lint
ruff check .
ruff format .

# Type check
mypy git_ai_commit/
```

---

## 📋 FAQ

**Q: Is my code sent to the cloud?**

A: If you use OpenAI or Anthropic, yes — only the diff (not your full codebase) is sent. With Ollama, everything stays local.

**Q: Does it work with any git repo?**

A: Yes! Any git repository with staged changes.

**Q: Can I use it with GitHub/GitLab?**

A: Absolutely. It creates standard git commits that work with any remote.

**Q: What if I don't have an API key?**

A: Use Ollama — it's free and runs locally.

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
# Fork, clone, create branch
git checkout -b feat/my-feature

# Make changes, test
pytest

# Submit PR
```

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built with ❤️ by [Nous Research](https://nousresearch.com)**

If this tool saves you time, give it a ⭐!

[⬆ Back to top](#-git-ai-commit)

</div>
