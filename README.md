# Repowiki: Hierarchical Wiki Generator

Generate comprehensive hierarchical wiki documentation from code repositories using LightRAG knowledge graphs.

**✨ Works out of the box!** Uses GitHub Copilot models by default (same as `adk-python/lightrag_openspec`).

## 🚀 Quick Start

```bash
cd /home/hfeng1/repowiki
uv venv && source .venv/bin/activate
uv pip install -e .
repowiki all
```

**That's it!** No API keys, no authentication, no configuration needed.

## 📦 Installation

### Using UV (Recommended)

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

### Using pip

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## 🎯 Usage

### CLI Commands

```bash
# Test your setup
repowiki test

# Index repository
repowiki index

# Generate base wiki (fast, ~30 pages)
repowiki generate

# Generate extended wiki (comprehensive, ~70 pages)
repowiki generate --extended

# Generate with specific model
repowiki generate --model gpt-4o

# Run everything (index + generate)
repowiki all

# Run everything with extended wiki
repowiki all --extended

# Show all options
repowiki --help
```

### Python API

```python
from repowiki import Config, RepositoryIndexer, WikiGenerator

# Configure
config = Config(
    lightrag_repo="/home/hfeng1/lightrag",
    working_dir="lightrag_storage",
    output_dir="wiki_docs"
)

# Index repository
indexer = RepositoryIndexer(config)
await indexer.index_repository()

# Generate base wiki
generator = WikiGenerator(config)
await generator.generate_all()

# Generate extended wiki
generator = WikiGenerator(config, extended=True)
await generator.generate_all()
```

## 📁 Project Structure

```
repowiki/
├── src/repowiki/
│   ├── __init__.py         # Package exports
│   ├── config.py            # Configuration (GitHub Copilot defaults)
│   ├── indexer.py           # Repository indexer
│   ├── generator.py         # Wiki generator
│   ├── prompts.py           # Prompt templates
│   └── cli.py               # CLI interface
├── tests/
│   ├── test_config.py
│   ├── test_indexer.py
│   └── test_generator.py
└── Documentation
```

## 🎨 Features

✅ **Works out of the box** - No API keys or setup required  
✅ **GitHub Copilot models** - Same as adk-python/lightrag_openspec  
✅ **Hierarchical organization** - 3-4 level deep structure  
✅ **Smart query modes** - global, local, mix, hybrid, naive  
✅ **Breadcrumb navigation** - Easy to navigate  
✅ **Category indexes** - Table of contents for each section  
✅ **Fully customizable** - Edit prompts in `prompts.py`  
✅ **Clean architecture** - Modular, testable code  

## 📊 Output Structure

### Base Wiki (~30 pages)

```
wiki_docs/
├── README.md                    # Home page
└── 01-overview/                 # Overview & architecture
    ├── project-overview.md
    ├── architecture.md
    └── design-decisions.md
```

### Extended Wiki (~70 pages)

```
wiki_docs/
├── README.md                    # Home page
├── 01-overview/                 # Overview & architecture
├── 02-getting-started/          # Installation & quick start
├── 03-api-reference/            # API documentation
├── 04-storage-backends/         # Storage options
├── 05-llm-integration/          # LLM providers
└── 06-examples/                 # Usage examples
```

Use `repowiki generate --extended` for comprehensive documentation.

## 🔧 Configuration

### Default Configuration

By default, repowiki uses GitHub Copilot models (same as lightrag_openspec):

```python
llm_model_name = "github_copilot/gpt-4o-mini"
embedding_model_name = "github_copilot/text-embedding-3-small"
api_key = "oauth2"
```

**No setup required!** Just run `repowiki all`.

### Environment Variables (Optional)

```bash
export LIGHTRAG_REPO="/path/to/lightrag"
export LIGHTRAG_WORKING_DIR="./storage"
export LIGHTRAG_OUTPUT_DIR="./wiki"
export LIGHTRAG_LLM_MODEL="github_copilot/gpt-4o-mini"
export LIGHTRAG_EMBEDDING_MODEL="github_copilot/text-embedding-3-small"
```

### Custom Configuration

```python
from repowiki import Config

config = Config(
    lightrag_repo="/custom/path",
    llm_model_name="github_copilot/gpt-4o-mini",
    embedding_model_name="github_copilot/text-embedding-3-small",
    workspace="main"
)
```

## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=repowiki

# Specific test
pytest tests/test_config.py
```

## 📈 Performance

| Mode | Pages | Time | Cost |
|------|-------|------|------|
| Base | ~30 | 10-15 min | FREE |
| Extended | ~70 | 20-30 min | FREE |

**Note**: Times are with parallel processing enabled. Uses GitHub Copilot models (free).

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide
- **[INSTALL.md](INSTALL.md)** - Installation details
- **[MIGRATION.md](MIGRATION.md)** - Migration from old scripts
- **[REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md)** - Refactoring details

## 🎓 Same Configuration as lightrag_openspec

Repowiki uses the **exact same configuration** as `adk-python/lightrag_openspec`:

- ✅ GitHub Copilot models: `github_copilot/gpt-4o-mini`
- ✅ Embedding model: `github_copilot/text-embedding-3-small`
- ✅ API key: `oauth2` (hardcoded)
- ✅ No authentication required
- ✅ Works out of the box

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure tests pass
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

Built with [LightRAG](https://github.com/HKUDS/LightRAG) - Simple and Fast Retrieval-Augmented Generation

---

**No setup, just works!** Same configuration as `adk-python/lightrag_openspec`. 🚀
