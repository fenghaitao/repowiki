# Repowiki: Hierarchical Wiki Generator

Generate comprehensive hierarchical wiki documentation from **any code repository** using LightRAG knowledge graphs.

**✨ Works out of the box!** Uses GitHub Copilot models by default. Works with any git repository.

## 🚀 Quick Start

```bash
# Install
pip install lightrag
cd /path/to/your/project

# Generate wiki
repowiki all --extended
```

**That's it!** No API keys, no authentication, no configuration needed.

## 📦 Installation

```bash
# Install LightRAG
pip install lightrag

# Install repowiki
pip install repowiki
# Or from source:
git clone https://github.com/yourusername/repowiki
cd repowiki
pip install -e .
```

## 🎯 Usage

### CLI Commands

```bash
# Test your setup
repowiki test

# Index current directory
cd /path/to/your/project
repowiki index

# Index specific repository
repowiki index --repo /path/to/project

# Generate base wiki (fast, ~13 pages)
repowiki generate

# Generate extended wiki (comprehensive, ~19 pages)
repowiki generate --extended

# Generate with specific model
repowiki generate --model gpt-4o

# Run everything (index + generate)
repowiki all --extended

# Show all options
repowiki --help
```

### Python API

```python
from repowiki import Config, RepositoryIndexer, WikiGenerator

# Configure (uses current directory by default)
config = Config(
    repo_path=".",  # Current directory
    working_dir="repowiki_storage",
    output_dir="wiki_docs"
)

# Or specify a repository
config = Config(repo_path="/path/to/project")

# Index repository
indexer = RepositoryIndexer(config)
await indexer.index_repository()

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

✅ **Works with any repository** - Not limited to specific projects  
✅ **Auto-detects repo name** - From git remote or directory name  
✅ **Works out of the box** - No API keys or setup required  
✅ **GitHub Copilot models** - Free with GitHub Copilot license  
✅ **Maximum parallel processing** - Optimized for Business license (4x faster)  
✅ **Hierarchical organization** - 3-4 level deep structure  
✅ **Smart query modes** - global, local, mix, hybrid, naive  
✅ **Breadcrumb navigation** - Easy to navigate  
✅ **Category indexes** - Table of contents for each section  
✅ **Fully customizable** - Edit prompts in `prompts.py`  
✅ **Clean architecture** - Modular, testable code  

## 📊 Output Structure

### Base Wiki (~13 pages)

```
wiki_docs/
├── README.md                    # Home page
└── 01-overview/                 # Overview & architecture
    ├── README.md
    ├── project-overview.md
    ├── architecture.md
    └── design-decisions.md
```

### Extended Wiki (~19 pages)

```
wiki_docs/
├── README.md                    # Home page
├── 01-overview/                 # Overview & architecture
├── 02-getting-started/          # Installation & configuration
├── 03-core-concepts/            # Key components & workflows
├── 04-api-reference/            # Public API & examples
└── 05-development/              # Dependencies, testing, extensions
```

Use `repowiki generate --extended` for comprehensive documentation.

## 🔧 Configuration

### Default Configuration

By default, repowiki uses GitHub Copilot models and current directory:

```python
repo_path = Path(".")  # Current directory
working_dir = Path("./repowiki_storage")
output_dir = Path("./wiki_docs")
llm_model_name = "github_copilot/gpt-4o"
embedding_model_name = "github_copilot/text-embedding-3-small"
api_key = "oauth2"
```

**No setup required!** Just run `repowiki all` in your project directory.

### Environment Variables (Optional)

```bash
export REPO_PATH="/path/to/project"
export WORKING_DIR="./storage"
export OUTPUT_DIR="./wiki"
export REPO_NAME="My Project"
export LLM_MODEL="github_copilot/gpt-4o"
export EMBEDDING_MODEL="github_copilot/text-embedding-3-small"
```

### Custom Configuration

```python
from repowiki import Config

config = Config(
    repo_path="/path/to/project",
    repo_name="My Awesome Project",
    llm_model_name="github_copilot/gpt-4o",
    embedding_model_name="github_copilot/text-embedding-3-small"
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

# Test setup (checks if everything is configured correctly)
repowiki test
```

**Note**: The indexer skips files smaller than 50 bytes by default. Adjust with `MIN_FILE_SIZE` environment variable if needed.

### Troubleshooting

**Pipmaster Warning**: You may see this warning when running commands:
```
pipmaster.package_manager - ERROR - Command failed with exit code 1: ... -m pip install --upgrade llama-index
```

This is **harmless and can be ignored**. The script uses `llama-index-core` (which is correctly installed), but `pipmaster` (part of `lightrag-hku`) tries to check for the old `llama-index` package name. The script will continue to work normally despite this warning.

## 📈 Performance

| Mode | Pages | Time | Cost |
|------|-------|------|------|
| Base | ~13 | 2-3 min | FREE |
| Extended | ~19 | 5-10 min | FREE |

**Indexing**: ~10 hours for 135 files (first time, includes entity merging)  
**Generation**: ~30 seconds (with warm cache)

**Note**: Uses GitHub Copilot models (free with license). Optimized for GitHub Copilot Business license with ultra-aggressive parallelism (48/96/48).

## 📚 Documentation

- **[GENERIC_REPO_SUPPORT.md](GENERIC_REPO_SUPPORT.md)** - Generic repository support
- **[PROMPT_REFINEMENT_SUMMARY.md](PROMPT_REFINEMENT_SUMMARY.md)** - Prompt improvements
- **[GENERATION_RESULTS_COMPARISON.md](GENERATION_RESULTS_COMPARISON.md)** - Performance results
- **[GITHUB_COPILOT_BUSINESS_OPTIMAL_SETTINGS.md](GITHUB_COPILOT_BUSINESS_OPTIMAL_SETTINGS.md)** - Parallel settings

## 🎓 Same Configuration as lightrag_openspec

Repowiki uses the **exact same configuration** as `adk-python/lightrag_openspec`:

- ✅ GitHub Copilot models: `github_copilot/gpt-4o`
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

**Works with any repository!** No setup, just works. 🚀
