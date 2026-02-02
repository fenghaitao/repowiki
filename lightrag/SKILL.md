---
name: repowiki
description: Generate comprehensive hierarchical wiki documentation from any code repository using LightRAG knowledge graphs. Supports repository indexing, intelligent querying, and automated wiki generation with multiple modes (base/extended).
homepage: https://github.com/fenghaitao/repowiki
metadata: {"clawdbot":{"emoji":"📚","requires":{"bins":["uv"]}}}
---

# RepoWiki - LightRAG Wiki Generator

Generate comprehensive hierarchical wiki documentation from any code repository using LightRAG knowledge graphs.

## Quick Start

### Generate Wiki from Current Repository
```bash
# Test setup
uv run {baseDir}/scripts/repowiki.py test

# Index and generate wiki (all-in-one)
uv run {baseDir}/scripts/repowiki.py all --extended

# Basic wiki (faster, ~13 pages)
uv run {baseDir}/scripts/repowiki.py all
```

### Index Specific Repository
```bash
uv run {baseDir}/scripts/repowiki.py index --repo /path/to/project
```

### Generate from Existing Index
```bash
uv run {baseDir}/scripts/repowiki.py generate --extended
```

## Features

✅ **Works with any repository** - Not limited to specific projects  
✅ **Auto-detects repo name** - From git remote or directory name  
✅ **Works out of the box** - Uses GitHub Copilot models by default  
✅ **Maximum parallel processing** - Optimized for GitHub Copilot Business  
✅ **Hierarchical organization** - 3-4 level deep structure  
✅ **Smart query modes** - global, local, mix, hybrid, naive  
✅ **Breadcrumb navigation** - Easy to navigate  
✅ **Category indexes** - Table of contents for each section  

## Commands

### Test Setup
```bash
uv run {baseDir}/scripts/repowiki.py test
```
Validates configuration, checks dependencies, and verifies repository access.

### Index Repository
```bash
# Index current directory
uv run {baseDir}/scripts/repowiki.py index

# Index specific repository
uv run {baseDir}/scripts/repowiki.py index --repo /path/to/project

# Custom working directory
uv run {baseDir}/scripts/repowiki.py index --working-dir ./storage
```

### Generate Wiki
```bash
# Base wiki (~13 pages, faster)
uv run {baseDir}/scripts/repowiki.py generate

# Extended wiki (~19 pages, comprehensive)
uv run {baseDir}/scripts/repowiki.py generate --extended

# Custom model
uv run {baseDir}/scripts/repowiki.py generate --model gpt-4o

# Custom output directory
uv run {baseDir}/scripts/repowiki.py generate --output ./wiki
```

### All-in-One (Index + Generate)
```bash
# Base wiki
uv run {baseDir}/scripts/repowiki.py all

# Extended wiki (recommended)
uv run {baseDir}/scripts/repowiki.py all --extended

# Specific repository
uv run {baseDir}/scripts/repowiki.py all --repo /path/to/project --extended
```

## Wiki Structure

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

## Configuration

### Environment Variables (Optional)

```bash
export REPO_PATH="/path/to/project"
export WORKING_DIR="./repowiki_storage"
export OUTPUT_DIR="./wiki_docs"
export REPO_NAME="My Project"
export LLM_MODEL="github_copilot/gpt-4o"
export EMBEDDING_MODEL="github_copilot/text-embedding-3-small"
```

### Default Configuration

Uses GitHub Copilot models by default (free with GitHub Copilot license):

- **LLM Model**: `github_copilot/gpt-4o` (128K context)
- **Embedding Model**: `github_copilot/text-embedding-3-small`
- **API Key**: `oauth2` (automatic with GitHub Copilot)
- **Working Directory**: `./repowiki_storage`
- **Output Directory**: `./wiki_docs`

### Custom Model Configuration

```bash
# Use different model
uv run {baseDir}/scripts/repowiki.py generate --model gpt-4o-mini

# Or set environment variable
export LLM_MODEL="gpt-4o-mini"
uv run {baseDir}/scripts/repowiki.py generate
```

## Query Modes

The knowledge graph supports multiple query modes:

- **global** - Search across entire codebase
- **local** - Focus on specific components
- **mix** - Combine global and local context
- **hybrid** - Balance breadth and depth
- **naive** - Simple keyword search

The generator automatically selects appropriate modes for different sections.

## Performance

| Mode | Pages | Time | Cost |
|------|-------|------|------|
| Base | ~13 | 2-3 min | FREE |
| Extended | ~19 | 5-10 min | FREE |

**Indexing**: First-time indexing may take longer for large repositories  
**Generation**: ~30 seconds with warm cache  
**Parallelism**: Optimized for GitHub Copilot Business (48/96/48 concurrent calls)

## Examples

### Document Your Own Project
```bash
cd /path/to/your/project
uv run /path/to/lightrag/scripts/repowiki.py all --extended
```

### Document Open Source Project
```bash
git clone https://github.com/user/project
cd project
uv run /path/to/lightrag/scripts/repowiki.py all --extended
```

### Re-generate After Code Changes
```bash
# Re-index updated files
uv run {baseDir}/scripts/repowiki.py index

# Generate fresh wiki
uv run {baseDir}/scripts/repowiki.py generate --extended
```

## File Support

By default, indexes:
- **Python files**: `.py`
- **Markdown files**: `.md`
- **Text files**: `.txt`

Skips files smaller than 50 bytes (configurable via `MIN_FILE_SIZE` environment variable).

## Troubleshooting

### Check Setup
```bash
uv run {baseDir}/scripts/repowiki.py test
```

### Common Issues

**Repository not found**
```bash
# Specify path explicitly
uv run {baseDir}/scripts/repowiki.py index --repo /full/path/to/project
```

**Import errors**
```bash
# Reinstall dependencies
uv pip install lightrag-hku openai tiktoken numpy networkx
```

**GitHub Copilot not working**
- Ensure you have an active GitHub Copilot license
- Check that you're signed in to GitHub in your IDE
- Try using a different model: `--model gpt-4o-mini`

## Output Files

After generation, you'll find:

```
repowiki_storage/     # Knowledge graph storage (internal)
  └── main/           # Default workspace
      ├── kv_store_*.json
      ├── graph_chunk_*.json
      └── ...

wiki_docs/            # Generated wiki documentation
  ├── README.md       # Start here!
  ├── 01-overview/
  ├── 02-getting-started/
  └── ...
```

## Advanced Usage

### Custom Parallel Processing

```bash
export MAX_PARALLEL_INSERT=48
export LLM_MODEL_MAX_ASYNC=96
export EMBEDDING_FUNC_MAX_ASYNC=48
uv run {baseDir}/scripts/repowiki.py all --extended
```

### Custom File Extensions

Edit the script's `code_extensions` configuration to include additional file types.

### Multiple Workspaces

```bash
# Different workspace for experimental features
export WORKSPACE="experimental"
uv run {baseDir}/scripts/repowiki.py index --repo /path/to/project
```

## Integration

### Git Hooks

Add to `.git/hooks/post-commit`:
```bash
#!/bin/bash
uv run /path/to/lightrag/scripts/repowiki.py all --extended
```

### CI/CD Pipeline

```yaml
- name: Generate Wiki
  run: |
    pip install repowiki
    repowiki all --extended
    
- name: Deploy Wiki
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./wiki_docs
```

## Technical Details

**Built with:**
- [LightRAG](https://github.com/HKUDS/LightRAG) - Knowledge graph framework
- GitHub Copilot models - LLM and embeddings
- NetworkX - Graph operations
- Nano-VectorDB - Vector storage

**Architecture:**
1. **Indexer** - Scans repository, builds knowledge graph
2. **Generator** - Queries graph, generates hierarchical documentation
3. **Knowledge Graph** - Stores entities, relationships, and context

## References

See `references/` directory for additional documentation:
- Query modes and strategies
- Performance optimization
- Prompt customization
- Knowledge graph structure

## Related Skills

- **pptx-creator** - Generate presentations from wiki content
- **github-pr** - Create PRs with wiki updates
- **excel** - Export wiki metrics to spreadsheets
