"""Repository indexer - builds knowledge graph from codebase"""
import sys
import os
from pathlib import Path
from typing import List, Tuple, Optional
import asyncio

from .config import Config


class RepositoryIndexer:
    """Indexes a code repository into a LightRAG knowledge graph"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.config.validate()
        
        # Set API key in environment
        os.environ["OPENAI_API_KEY"] = self.config.api_key
        
        # Import LightRAG (assumes it's installed via pip)
        from lightrag import LightRAG
        from lightrag.llm.llama_index_impl import (
            llama_index_complete_if_cache,
            llama_index_embed,
        )
        from lightrag.utils import EmbeddingFunc
        from llama_index.llms.litellm import LiteLLM
        from llama_index.embeddings.litellm import LiteLLMEmbedding
        
        self.EmbeddingFunc = EmbeddingFunc
        self.LightRAG = LightRAG
        self.llama_index_complete_if_cache = llama_index_complete_if_cache
        self.llama_index_embed = llama_index_embed
        self.LiteLLM = LiteLLM
        self.LiteLLMEmbedding = LiteLLMEmbedding
        
        print(f"🤖 Using GitHub Copilot models")
        print(f"   LLM: {self.config.llm_model_name}")
        print(f"   Embedding: {self.config.embedding_model_name}")
        
        self.rag = None
    
    async def _create_llm_func(self, prompt, system_prompt=None, history_messages=[], **kwargs):
        """Create LLM function using LiteLLM."""
        if "llm_instance" not in kwargs:
            kwargs["llm_instance"] = self.LiteLLM(
                model=self.config.llm_model_name,
                api_key=self.config.api_key,
                temperature=0.7,
            )
        return await self.llama_index_complete_if_cache(
            kwargs["llm_instance"], prompt, system_prompt, history_messages
        )
    
    async def _create_embedding_func(self, texts):
        """Create embedding function using LiteLLM."""
        embed_model = self.LiteLLMEmbedding(
            model_name=self.config.embedding_model_name,
            api_key=self.config.api_key,
        )
        return await self.llama_index_embed(texts, embed_model=embed_model)
    
    async def initialize_rag(self):
        """Initialize LightRAG instance"""
        # Wrap embedding function with EmbeddingFunc
        embedding_func_wrapped = self.EmbeddingFunc(
            embedding_dim=1536,  # text-embedding-3-small dimension
            max_token_size=8192,
            func=self._create_embedding_func,
        )
        
        self.rag = self.LightRAG(
            working_dir=str(self.config.working_dir),
            workspace=self.config.workspace,
            llm_model_func=self._create_llm_func,
            embedding_func=embedding_func_wrapped,
            llm_model_name=self.config.llm_model_name,
            # Parallel processing configuration (configurable)
            max_parallel_insert=self.config.max_parallel_insert,
            llm_model_max_async=self.config.llm_model_max_async,
            embedding_func_max_async=self.config.embedding_func_max_async,
        )
        # Initialize storages (required for JsonDocStatusStorage)
        await self.rag.initialize_storages()
        return self.rag
    
    def collect_files(self) -> List[Path]:
        """Collect files to index from repository"""
        repo_path = Path(self.config.repo_path)
        
        # File patterns to include (code and docs only)
        include_patterns = ['*.py', '*.md', '*.txt']
        
        # Directories to exclude
        exclude_dirs = {
            '__pycache__', '.pytest_cache', 'node_modules',
            'venv', 'build', 'dist', '*.egg-info'
        }
        
        files = []
        for pattern in include_patterns:
            for file_path in repo_path.rglob(pattern):
                # Skip if in excluded directory
                if any(excluded in file_path.parts for excluded in exclude_dirs):
                    continue
                
                # Skip any directory starting with "." (hidden directories)
                if any(part.startswith('.') for part in file_path.parts):
                    continue
                    
                # Skip if too small
                if file_path.stat().st_size < self.config.min_file_size:
                    continue
                    
                files.append(file_path)
        
        return sorted(files)
    
    async def read_file_content(self, file_path: Path) -> Tuple[bool, Optional[str], Optional[str]]:
        """Read and prepare file content for indexing
        
        Returns:
            Tuple of (success: bool, content: str, rel_path: str)
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Skip if content too small
            if len(content.strip()) < self.config.min_file_size:
                return False, None, None
            
            # Get relative path for better context
            rel_path = file_path.relative_to(self.config.repo_path)
            
            # Add file context to content
            full_content = f"# File: {rel_path}\n\n{content}"
            
            return True, full_content, str(rel_path)
            
        except Exception as e:
            print(f"   ✗ Error reading {file_path.name}: {e}")
            return False, None, None
    
    async def index_repository(self) -> Tuple[int, int, int]:
        """Index entire repository using parallel batch processing
        
        Returns:
            Tuple of (indexed_count, skipped_count, error_count)
        """
        print("=" * 80)
        print("INDEXING REPOSITORY (PARALLEL MODE)")
        print("=" * 80)
        
        # Initialize RAG
        await self.initialize_rag()
        
        print(f"⚡ Parallel processing enabled:")
        print(f"   - max_parallel_insert: {self.rag.max_parallel_insert}")
        print(f"   - llm_model_max_async: {self.rag.llm_model_max_async}")
        print(f"   - embedding_func_max_async: {self.rag.embedding_func_max_async}")
        print()
        
        # Collect files
        files_to_index = self.collect_files()
        print(f"📁 Found {len(files_to_index)} files to index")
        print()
        
        # Read all file contents
        print("📖 Reading files...")
        read_tasks = [self.read_file_content(f) for f in files_to_index]
        read_results = await asyncio.gather(*read_tasks)
        
        # Separate successful reads from failures
        contents = []
        file_paths = []
        skipped_count = 0
        
        for (success, content, rel_path) in read_results:
            if success:
                contents.append(content)
                file_paths.append(rel_path)
            else:
                skipped_count += 1
        
        print(f"✅ Successfully read {len(contents)} files")
        print(f"⏭️  Skipped {skipped_count} files (too small or errors)")
        print()
        
        if not contents:
            print("⚠️  No files to index!")
            return 0, skipped_count, 0
        
        # Use LightRAG's batch insert with automatic parallelization
        print(f"🚀 Starting parallel batch indexing of {len(contents)} files...")
        print(f"   This will process up to {self.rag.max_parallel_insert} documents concurrently")
        print()
        
        try:
            # LightRAG will automatically handle parallel processing
            await self.rag.ainsert(
                contents,
                file_paths=file_paths,
            )
            
            indexed_count = len(contents)
            error_count = 0
            
        except Exception as e:
            print(f"\n❌ Error during batch indexing: {e}")
            # Fall back to individual processing if batch fails
            print("\n🔄 Falling back to individual file processing...")
            indexed_count = 0
            error_count = 0
            
            for i, (content, file_path) in enumerate(zip(contents, file_paths), 1):
                try:
                    await self.rag.ainsert(content, file_paths=file_path)
                    indexed_count += 1
                    if i % 10 == 0:
                        print(f"   ✓ Processed {i}/{len(contents)} files...")
                except Exception as e:
                    print(f"   ✗ Error indexing {file_path}: {e}")
                    error_count += 1
        
        print("\n" + "=" * 80)
        print("INDEXING COMPLETE")
        print("=" * 80)
        print(f"✅ Successfully indexed: {indexed_count} files")
        print(f"⏭️  Skipped: {skipped_count} files (too small)")
        print(f"❌ Errors: {error_count} files")
        print(f"📁 Storage: {self.config.working_dir}")
        print("=" * 80)
        
        return indexed_count, skipped_count, error_count


async def main():
    """CLI entry point for indexer"""
    config = Config.from_env()
    indexer = RepositoryIndexer(config)
    await indexer.index_repository()


if __name__ == "__main__":
    asyncio.run(main())
