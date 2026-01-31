#!/usr/bin/env python3
"""
Step 1: Index the LightRAG repository into a knowledge graph
"""
import os
import sys
import asyncio
from pathlib import Path

# Add LightRAG to path - adjust this to point to the LightRAG directory
LIGHTRAG_REPO = Path("/home/hfeng1/lightrag")  # Update this path if different
sys.path.insert(0, str(LIGHTRAG_REPO))

from lightrag import LightRAG, QueryParam
from lightrag.llm import openai_complete_if_cache, openai_embedding


async def index_repository():
    """Index the LightRAG repository"""
    
    print("=" * 80)
    print("STEP 1: Indexing LightRAG Repository")
    print("=" * 80)
    
    # Initialize LightRAG
    working_dir = Path(__file__).parent / "lightrag_storage"
    working_dir.mkdir(exist_ok=True)
    
    print(f"\n📁 Working directory: {working_dir}")
    print(f"📂 Repository path: {LIGHTRAG_REPO}")
    
    rag = LightRAG(
        working_dir=str(working_dir),
        workspace="main",
        llm_model_func=openai_complete_if_cache,
        embedding_func=openai_embedding
    )
    
    # File extensions to index
    code_extensions = {'.py', '.md', '.yaml', '.yml', '.json', '.txt', '.toml'}
    
    # Directories to skip
    skip_dirs = {
        '__pycache__', '.git', '.pytest_cache', 'node_modules',
        '.venv', 'venv', 'env', '.eggs', '*.egg-info',
        'build', 'dist', '.tox', 'htmlcov', '.mypy_cache',
        'lightrag_webui', 'assets', 'examples/unofficial-sample'
    }
    
    # Collect files to index
    files_to_index = []
    
    print("\n🔍 Scanning repository for files...")
    
    for root, dirs, files in os.walk(LIGHTRAG_REPO):
        # Skip directories
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if any(file.endswith(ext) for ext in code_extensions):
                if not file.startswith('.'):
                    file_path = Path(root) / file
                    files_to_index.append(file_path)
    
    print(f"✅ Found {len(files_to_index)} files to index")
    
    # Index files
    indexed_count = 0
    skipped_count = 0
    error_count = 0
    
    print("\n📚 Indexing files...\n")
    
    for file_path in files_to_index:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if len(content.strip()) < 50:
                skipped_count += 1
                continue
            
            rel_path = file_path.relative_to(LIGHTRAG_REPO)
            
            file_header = f"""# File: {rel_path}
# Type: {file_path.suffix}
# Path: {rel_path.parent}

"""
            full_content = file_header + content
            
            await rag.ainsert(full_content)
            
            indexed_count += 1
            
            if indexed_count % 10 == 0:
                print(f"   ✓ Indexed {indexed_count}/{len(files_to_index)} files...")
        
        except Exception as e:
            error_count += 1
            print(f"   ✗ Error indexing {file_path.name}: {e}")
    
    print("\n" + "=" * 80)
    print("📊 INDEXING COMPLETE")
    print("=" * 80)
    print(f"✅ Successfully indexed: {indexed_count} files")
    print(f"⏭️  Skipped: {skipped_count} files")
    print(f"❌ Errors: {error_count} files")
    print(f"📁 Storage: {working_dir}")
    print("=" * 80)
    
    return rag, working_dir


if __name__ == "__main__":
    asyncio.run(index_repository())
