# RepoWiki - LightRAG Wiki Generator Skill

This ClawdHub skill generates comprehensive hierarchical wiki documentation from any code repository using LightRAG knowledge graphs.

Source: https://github.com/fenghaitao/repowiki

## What This Skill Does

- **Indexes repositories** into LightRAG knowledge graphs
- **Generates hierarchical wiki** with 3-4 levels of organization
- **Supports multiple query modes** (global, local, mix, hybrid, naive)
- **Works out of the box** with GitHub Copilot models
- **Auto-detects repository info** from git or directory name

## Quick Test

```bash
# Test the skill
cd /path/to/any/repository
uv run lightrag-apps/scripts/repowiki.py test

# Generate wiki
uv run lightrag-apps/scripts/repowiki.py all --extended
```

## Files Created

- `SKILL.md` - Complete documentation for the skill
- `_meta.json` - Metadata for ClawdHub skill registry
- `scripts/repowiki.py` - Main script (804 lines)
- `references/query-modes.md` - LightRAG query mode documentation
- `references/configuration.md` - Configuration guide

## Key Features

✅ Self-contained script with PEP 723 dependencies
✅ Works with any git repository
✅ GitHub Copilot integration (free with license)
✅ Optimized parallel processing (48/96/48)
✅ Base mode (~13 pages) and Extended mode (~19 pages)
✅ Complete CLI with test, index, generate, and all commands

## Differences from pptx-creator

This skill follows the pptx-creator pattern but adapts it for wiki generation:

1. **Single main script** instead of multiple specialized scripts
2. **Async operations** for LightRAG integration
3. **Knowledge graph** instead of template-based generation
4. **Hierarchical structure** instead of slide layouts
5. **Query modes** instead of chart types

## Usage Examples

See SKILL.md for complete documentation with all commands and options.

## Integration

Can be used with other dbhurley skills:
- Generate wiki docs, then create presentations with **pptx-creator**
- Export metrics with **excel** skill
- Create PRs with **github-pr** skill

## Technical Stack

- LightRAG for knowledge graphs
- GitHub Copilot for LLM/embeddings
- NetworkX for graph operations
- Async/await for performance
