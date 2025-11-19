# QuantCoder CLI v1.0.0 - Testing Guide

## 🎉 Installation Complete!

Your QuantCoder CLI is now installed with all security improvements and modernizations.

---

## ✅ What's Been Improved

### Critical Bug Fixes
- ✅ Added missing `requests` import in `utils.py`
- ✅ Fixed OpenAI SDK migration (0.28 → 1.x+)
- ✅ Added LLMClient abstraction layer

### Security Enhancements
- ✅ URL validation before opening in browser
- ✅ `validate_url()` function to check URL safety
- ✅ Blocks unsafe URLs (javascript:, ftp:, etc.)
- ✅ Environment variable support for sensitive data

### Architecture Improvements
- ✅ OpenAI SDK 1.x+ with proper error handling
- ✅ Lazy tkinter imports (no GUI dependency for CLI)
- ✅ Defensive programming patterns in code generation
- ✅ Token usage tracking

---

## 🚀 Quick Start

### 1. Activate Virtual Environment

```bash
source .venv/bin/activate
```

### 2. Download spaCy Language Model (Required)

```bash
# Try direct download
python -m spacy download en_core_web_sm

# If that fails, use pip
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-tar.gz
```

### 3. Configure Environment Variables

```bash
# Copy example file
cp .env.example .env

# Edit .env and add your API key
nano .env  # or use your preferred editor
```

Required in `.env`:
```bash
OPENAI_API_KEY=your_actual_openai_api_key_here
```

Optional:
```bash
OPENAI_MODEL=gpt-4o-2024-11-20
UNPAYWALL_EMAIL=your.email@example.com
MAX_REFINE_ATTEMPTS=6
```

---

## 🧪 Testing the CLI

### Test 1: Basic Commands

```bash
# Activate environment
source .venv/bin/activate

# Test help
quantcli --help

# Test hello command
quantcli hello
```

**Expected Output:**
```
Hello from QuantCLI!
```

### Test 2: Search for Articles

```bash
quantcli search "algorithmic trading momentum" --num 3
```

**Expected Output:**
- List of 3 articles from CrossRef
- Articles saved to `articles.json`
- Option to save to HTML

**Security Test:** URLs are validated before opening in browser.

### Test 3: List Saved Articles

```bash
quantcli list
```

**Expected Output:**
- Shows previously searched articles from `articles.json`

### Test 4: Download Article PDF

```bash
quantcli download 1
```

**Expected Output:**
- PDF downloaded to `downloads/article_1.pdf`, OR
- Prompt to open article URL in browser (with URL validation)

### Test 5: Generate Trading Code from PDF

```bash
# First, make sure you have a PDF in downloads/
quantcli generate-code 1
```

**Expected Output:**
- Article summary displayed
- QuantConnect algorithm code generated
- Code saved to `generated_code/algorithm_1.py`

### Test 6: Interactive Mode (GUI)

```bash
quantcli interactive
```

**Expected Output:**
- GUI window opens (requires tkinter)
- Search interface with article list
- URL validation before opening articles

**If tkinter not available:**
```
⚠️  Interactive mode requires tkinter (GUI library)
Install with: sudo apt-get install python3-tk
```

---

## 🔒 Security Testing

### Test URL Validation

Create a test script:

```bash
source .venv/bin/activate
python << 'EOF'
from quantcli.utils import validate_url

test_cases = [
    ("https://example.com", True, "Valid HTTPS URL"),
    ("http://google.com", True, "Valid HTTP URL"),
    ("javascript:alert(1)", False, "XSS attempt blocked"),
    ("ftp://example.com", False, "Unsafe protocol blocked"),
    ("", False, "Empty string blocked"),
    ("not-a-url", False, "Invalid format blocked"),
]

print("🔒 Security Test Results:\n")
for url, expected, description in test_cases:
    result = validate_url(url)
    status = "✅ PASS" if result == expected else "❌ FAIL"
    print(f"{status}: {description}")
    print(f"   URL: '{url}' → {result}")
    print()
EOF
```

**Expected:** All tests should PASS.

---

## 📊 Verification Checklist

After testing, verify:

- [ ] CLI commands work (help, hello, search)
- [ ] Article search returns results
- [ ] URL validation blocks unsafe URLs
- [ ] OpenAI API key is loaded from .env
- [ ] PDF download attempts work
- [ ] Code generation produces valid Python
- [ ] No errors about missing imports
- [ ] spaCy model is installed

---

## 🐛 Troubleshooting

### Issue: "Module not found" errors

**Solution:**
```bash
source .venv/bin/activate
pip install -e .
```

### Issue: spaCy model not found

**Solution:**
```bash
source .venv/bin/activate
python -m spacy download en_core_web_sm
```

### Issue: OpenAI API errors

**Solution:**
- Check `.env` file has valid `OPENAI_API_KEY`
- Verify API key has credits: https://platform.openai.com/usage
- Check you're using OpenAI SDK 1.x+ (run `pip show openai`)

### Issue: tkinter not available

**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS (should be included)
# No action needed

# Use CLI commands instead of interactive mode
quantcli search "query" --num 5
```

### Issue: PDF download fails

**Reason:** Many academic articles are behind paywalls.

**Solution:**
- Use `quantcli open-article <ID>` to manually download
- Set `UNPAYWALL_EMAIL` in `.env` for open access attempts

---

## 📝 Example Workflow

Complete workflow to generate a trading algorithm:

```bash
# 1. Activate environment
source .venv/bin/activate

# 2. Search for articles
quantcli search "momentum trading strategy" --num 5

# 3. List results
quantcli list

# 4. Download an article (e.g., #1)
quantcli download 1

# 5. Generate algorithm from PDF
quantcli generate-code 1

# 6. Check generated code
cat generated_code/algorithm_1.py
```

---

## 🔄 Switching Branches

You're currently on: `refactor/modernize-2025`

To switch to the remote branch with all improvements:

```bash
# Option 1: Stay on current branch (already has all improvements)
git status

# Option 2: Track remote branch explicitly
git checkout claude/refactor-modernize-2025-011CV1sadPRrxj5sPHjWp7Wa

# Option 3: Create your own branch from current state
git checkout -b my-testing-branch
```

---

## 📚 Additional Resources

- **CHANGELOG.md** - Full list of changes
- **README.md** - Project overview
- **.env.example** - Configuration options
- **quantcli/llm_client.py** - New LLM abstraction layer

---

## 🎯 Next Steps

1. ✅ Install spaCy model: `python -m spacy download en_core_web_sm`
2. ✅ Configure `.env` with your OpenAI API key
3. ✅ Run test workflow above
4. ✅ Try generating code from a real PDF
5. ✅ Report any issues on GitHub

---

## 📧 Need Help?

If you encounter issues:

1. Check this guide's Troubleshooting section
2. Review logs in `quantcli.log`
3. Run with `--verbose` flag: `quantcli --verbose search "query"`
4. Report issues at: https://github.com/SL-Mar/quantcoder-cli/issues

---

**Version:** 1.0.0
**Branch:** refactor/modernize-2025
**Python:** >= 3.9
**OpenAI SDK:** >= 1.0.0
