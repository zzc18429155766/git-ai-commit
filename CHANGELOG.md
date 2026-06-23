# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Nothing yet.

## [1.0.0] - 2025-01-15

### Added
- 🎯 Conventional Commits support (feat/fix/refactor/docs/chore/perf/test/style/ci/build)
- 🧠 Multi-backend AI support: OpenAI, Anthropic, Ollama
- 💬 Interactive mode with accept/edit/regenerate/quit
- ⚡ Auto-commit mode (`--auto`)
- 📝 Commit message body generation
- 🎨 Rich terminal UI with colors, panels, and tables
- ⚙️ `.git-ai-commit.yml` configuration file
- 🌍 Multi-language commit message support
- 🔍 Breaking change detection
- 🏷️ Automatic scope detection
- 📦 Lightweight dependencies (click, rich, pyyaml, httpx)
- 🔧 Git subcommand support (`git ai-commit`)
- 🧪 Comprehensive test suite
- 📚 Full documentation with examples

### Supported AI Models
- OpenAI: gpt-4o, gpt-4o-mini, gpt-3.5-turbo
- Anthropic: claude-sonnet-4-20250514, claude-3-opus, claude-3-haiku
- Ollama: llama3.1, codellama, mistral, any Ollama model

---

## Release Notes

### 1.0.0 — Initial Release

The first stable release of git-ai-commit. A complete, production-ready CLI tool for generating beautiful conventional commit messages using AI.

**Key highlights:**
- Works as standalone `git-ai-commit` or git subcommand `git ai-commit`
- Supports three major AI backends with easy switching
- Beautiful terminal output powered by Rich
- Comprehensive configuration via YAML files and environment variables
- 100% type-annotated codebase with mypy strict mode

[Unreleased]: https://github.com/nousresearch/git-ai-commit/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/nousresearch/git-ai-commit/releases/tag/v1.0.0
