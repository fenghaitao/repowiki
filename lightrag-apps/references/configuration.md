# LightRAG Configuration Guide

## Environment Variables

All configuration can be done via environment variables:

```bash
# Repository settings
export REPO_PATH="/path/to/project"           # Default: current directory
export REPO_NAME="My Project"                 # Default: auto-detected from git

# Storage directories
export WORKING_DIR="./repowiki_storage"       # Default: ./repowiki_storage
export OUTPUT_DIR="./wiki_docs"               # Default: ./wiki_docs
export WORKSPACE="main"                       # Default: main

# LLM settings
export LLM_MODEL="github_copilot/gpt-4o"      # Default: github_copilot/gpt-4o
export EMBEDDING_MODEL="github_copilot/text-embedding-3-small"
export API_KEY="oauth2"                       # Default: oauth2 (for GitHub Copilot)

# Indexing settings
export MIN_FILE_SIZE="50"                     # Default: 50 bytes
export BATCH_REPORT_INTERVAL="10"             # Default: 10 files

# Parallel processing (optimized for GitHub Copilot Business)
export MAX_PARALLEL_INSERT="48"               # Default: 48
export LLM_MODEL_MAX_ASYNC="96"               # Default: 96
export EMBEDDING_FUNC_MAX_ASYNC="48"          # Default: 48
```

## Default Configuration

Works out of the box with GitHub Copilot:

- **LLM Model**: `github_copilot/gpt-4o` (128K context window)
- **Embedding Model**: `github_copilot/text-embedding-3-small` (1536 dimensions)
- **API Key**: `oauth2` (automatic authentication)
- **Repository**: Current directory (auto-detected)
- **Parallel Processing**: Ultra-aggressive (48/96/48)

## GitHub Copilot Models

### Supported Models

- `github_copilot/gpt-4o` - Recommended, 128K context (default)
- `github_copilot/gpt-4o-mini` - Faster, lower cost
- `github_copilot/gpt-4` - Legacy, 8K context
- `github_copilot/gpt-3.5-turbo` - Fast, basic tasks

### Embeddings

- `github_copilot/text-embedding-3-small` - 1536 dimensions (default)
- `github_copilot/text-embedding-3-large` - 3072 dimensions (higher quality)

## Alternative LLM Providers

### OpenAI

```bash
export LLM_MODEL="gpt-4o"
export EMBEDDING_MODEL="text-embedding-3-small"
export OPENAI_API_KEY="sk-..."
unset API_KEY  # Don't use oauth2
```

### Azure OpenAI

```bash
export LLM_MODEL="azure/gpt-4o"
export EMBEDDING_MODEL="azure/text-embedding-3-small"
export AZURE_API_KEY="..."
export AZURE_API_BASE="https://your-resource.openai.azure.com"
```

### Anthropic Claude

```bash
export LLM_MODEL="claude-3-opus-20240229"
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Performance Tuning

### Conservative Settings (Low Rate Limits)

```bash
export MAX_PARALLEL_INSERT="4"
export LLM_MODEL_MAX_ASYNC="8"
export EMBEDDING_FUNC_MAX_ASYNC="4"
```

### Moderate Settings (Standard Usage)

```bash
export MAX_PARALLEL_INSERT="12"
export LLM_MODEL_MAX_ASYNC="24"
export EMBEDDING_FUNC_MAX_ASYNC="12"
```

### Aggressive Settings (GitHub Copilot Business)

```bash
export MAX_PARALLEL_INSERT="48"
export LLM_MODEL_MAX_ASYNC="96"
export EMBEDDING_FUNC_MAX_ASYNC="48"
```

### Maximum Settings (Testing)

```bash
export MAX_PARALLEL_INSERT="64"
export LLM_MODEL_MAX_ASYNC="128"
export EMBEDDING_FUNC_MAX_ASYNC="64"
```

## File Type Configuration

By default, indexes: `.py`, `.md`, `.txt`

To add more file types, edit the script's `code_extensions` set:

```python
code_extensions: Set[str] = field(default_factory=lambda: {
    '.py', '.md', '.txt', '.js', '.ts', '.java', '.cpp', '.h'
})
```

## Repository Detection

### Automatic Detection

1. Tries `git remote get-url origin` to extract repo name
2. Falls back to directory name if git is unavailable

### Manual Override

```bash
export REPO_NAME="My Custom Project Name"
```

Or via command line:

```bash
# Not directly supported, but you can modify the script
# or use environment variables
```

## Working Directory Structure

```
repowiki_storage/
└── main/                          # Workspace (default: "main")
    ├── kv_store_full_docs.json    # Document storage
    ├── kv_store_text_chunks.json  # Text chunks
    ├── kv_store_llm_response_cache.json  # LLM cache
    ├── graph_chunk_entity_relation.graphml  # Entity graph
    ├── vdb_chunks.json            # Chunk vectors
    └── vdb_entities.json          # Entity vectors
```

## Output Directory Structure

```
wiki_docs/
├── README.md                      # Home page
├── 01-overview/
│   ├── README.md
│   ├── project-overview.md
│   ├── architecture.md
│   └── design-decisions.md
├── 02-getting-started/            # Extended mode only
│   └── ...
└── ...
```

## Multi-Workspace Usage

Use different workspaces for different purposes:

```bash
# Main documentation
export WORKSPACE="main"
uv run lightrag-apps/scripts/repowiki.py all --extended

# Experimental features branch
export WORKSPACE="experimental"
export REPO_PATH="/path/to/feature-branch"
uv run lightrag-apps/scripts/repowiki.py all

# Different versions
export WORKSPACE="v1.0"
export REPO_PATH="/path/to/v1.0"
uv run lightrag-apps/scripts/repowiki.py all
```

## Troubleshooting

### Rate Limiting

If you hit rate limits, reduce parallelism:

```bash
export MAX_PARALLEL_INSERT="8"
export LLM_MODEL_MAX_ASYNC="16"
export EMBEDDING_FUNC_MAX_ASYNC="8"
```

### Memory Issues

Reduce batch sizes and parallelism:

```bash
export MAX_PARALLEL_INSERT="4"
export BATCH_REPORT_INTERVAL="5"
```

### Slow Performance

Increase parallelism (if rate limits allow):

```bash
export MAX_PARALLEL_INSERT="64"
export LLM_MODEL_MAX_ASYNC="128"
```

### Authentication Issues

For GitHub Copilot:
- Ensure you're signed in to GitHub in your IDE
- Check that your Copilot license is active
- Try `oauth2` as API_KEY

For OpenAI:
- Set `OPENAI_API_KEY` environment variable
- Unset or remove `API_KEY="oauth2"`

## Best Practices

1. **Start with defaults** - They work well for most cases
2. **Use extended mode** - More comprehensive documentation
3. **Monitor first run** - Indexing takes time initially
4. **Cache is your friend** - Subsequent runs are much faster
5. **Test setup first** - Run `lightrag-apps/scripts/repowiki.py test` before indexing
6. **Backup storage** - Keep `repowiki_storage/` for faster regeneration
