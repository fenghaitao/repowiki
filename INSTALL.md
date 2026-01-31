# Installation Guide

## Using UV (Recommended)

UV is a fast Python package installer. This is the recommended method.

### 1. Install UV

If you don't have UV installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or via pip:

```bash
pip install uv
```

### 2. Create Virtual Environment and Install Dependencies

```bash
cd /home/hfeng1/repowiki

# Create venv and install dependencies
uv venv
source .venv/bin/activate
uv pip install -e .
```

Or install from requirements.txt:

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 3. Verify Installation

```bash
python3 test_setup.py
```

You should see all checks pass except OPENAI_API_KEY.

---

## Using Standard pip

If you prefer traditional pip:

```bash
cd /home/hfeng1/repowiki

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .
# Or: pip install -r requirements.txt
```

---

## Using Poetry

If you prefer Poetry:

```bash
cd /home/hfeng1/repowiki

# Install with Poetry
poetry install
poetry shell
```

---

## Development Installation

For development with all optional tools:

```bash
# With UV
uv pip install -e ".[dev]"

# With pip
pip install -e ".[dev]"
```

This installs:
- pytest (testing)
- ruff (linting)

---

## Verifying LightRAG Installation

The project needs the LightRAG repository. Verify it's accessible:

```bash
python3 -c "import sys; sys.path.insert(0, '/home/hfeng1/lightrag'); import lightrag; print('✅ LightRAG found')"
```

If this fails, either:
1. Install LightRAG: `pip install lightrag`
2. Or ensure `/home/hfeng1/lightrag` exists and is the correct path

---

## Setting Up API Keys

### OpenAI

```bash
export OPENAI_API_KEY="sk-your-key-here"

# Add to shell profile for persistence
echo 'export OPENAI_API_KEY="sk-your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### Alternative: Using Ollama (Free, Local)

If you want to use Ollama instead of OpenAI:

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull qwen2.5:7b

# Start Ollama server
ollama serve
```

Then I can help you modify the scripts to use Ollama instead of OpenAI.

---

## Quick Start After Installation

```bash
# Activate virtual environment
cd /home/hfeng1/repowiki
source .venv/bin/activate

# Test setup
python3 test_setup.py

# Set API key (if using OpenAI)
export OPENAI_API_KEY="sk-..."

# Generate wiki
python3 00_run_all.py
```

---

## Troubleshooting

### "uv: command not found"

Install UV first:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Restart your shell or run: source ~/.bashrc
```

### "No module named 'lightrag'"

Either:
```bash
pip install lightrag
```

Or ensure the LightRAG repo path is correct in `01_index_repository.py`.

### Virtual environment not activating

Make sure you're in the right directory:
```bash
cd /home/hfeng1/repowiki
source .venv/bin/activate
```

You should see `(.venv)` in your prompt.

### Import errors

Reinstall dependencies:
```bash
uv pip install --force-reinstall -r requirements.txt
```

---

## Directory Structure After Installation

```
repowiki/
├── .venv/                  # Virtual environment (created by uv/pip)
├── .python-version         # Python version specification
├── pyproject.toml          # Project metadata and dependencies
├── requirements.txt        # Dependency list
├── INSTALL.md              # This file
├── README.md               # Main documentation
├── SETUP.md                # Setup instructions
├── 00_run_all.py           # Main script
├── 01_index_repository.py  # Indexing script
├── 02_hierarchical_wiki_generator.py  # Wiki generator
└── test_setup.py           # Setup verification
```

---

## Next Steps

After installation:

1. ✅ Verify installation: `python3 test_setup.py`
2. ✅ Set API key: `export OPENAI_API_KEY="..."`
3. ✅ Generate wiki: `python3 00_run_all.py`

Happy documenting! 🚀
