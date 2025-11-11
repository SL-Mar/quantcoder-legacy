# Changelog

All notable changes to QuantCoder will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-11

### 🚀 Major Refactoring - OpenAI SDK Migration

#### Added
- **New LLMClient abstraction layer** (`quantcli/llm_client.py`)
  - Unified interface for all LLM interactions
  - Support for OpenAI SDK v1.x+
  - Standardized response format with `LLMResponse` dataclass
  - Improved error handling and logging
  - Token usage tracking

- **Test infrastructure**
  - pytest configuration
  - Unit tests for LLMClient
  - Coverage reporting (pytest-cov)
  - Test markers for unit/integration/slow tests

- **Modern dependencies**
  - OpenAI SDK >= 1.0.0
  - Rich terminal output library
  - Type checking with mypy
  - Code quality with ruff

#### Changed
- **Breaking**: Migrated from OpenAI SDK 0.28 to 1.x+
  - Replaced deprecated `openai.ChatCompletion.create()` calls
  - Updated all LLM interactions in `processor.py` to use LLMClient
  - Removed global `openai.api_key` configuration

- **Improved dependency management**
  - Bumped Python requirement to >= 3.9
  - Pin minimum versions for all dependencies
  - Created clean `requirements.txt` (removed legacy freeze)

- **Enhanced setup.py**
  - Version bumped to 1.0.0
  - Updated classifiers for PyPI
  - Improved project description
  - Added support for Python 3.9-3.12

#### Removed
- Direct `openai` module imports from utils.py
- Hardcoded global API key setting
- Legacy OpenAI 0.28 compatibility code

### Migration Guide

**For existing users upgrading from 0.3:**

1. Update your environment:
```bash
pip install --upgrade openai>=1.0.0
pip install -e .
```

2. No code changes required - the LLMClient abstraction handles SDK differences internally

3. Ensure `OPENAI_API_KEY` is set in your environment or `.env` file

### Technical Debt Addressed
- ✅ OpenAI SDK obsolescence (0.28 → 1.x+)
- ✅ Missing test coverage
- ✅ Lack of structured logging for LLM calls
- ✅ Token usage visibility

### Known Issues
- GUI module (gui.py) not yet updated - marked for deprecation
- End-to-end integration tests pending
- Documentation needs refresh for v1.0.0

---

## [0.3] - 2024-10-01

### Legacy Version
- Original CLI implementation
- OpenAI SDK 0.28
- Basic PDF processing and code generation
- CrossRef article search
- Interactive mode

