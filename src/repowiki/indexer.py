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
        
        # Add LightRAG to path
        sys.path.insert(0, str(self.config.lightrag_repo))
        
        # Set API key in environment (for LightRAG)
        os.environ["OPENAI_API_KEY"] = self.config.api_key
        
        # Import LightRAG
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
        
        print(f"🤖 Using GitHub Copilot models (like lightrag_openspec)")
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
        )
        # Initialize storages (required for JsonDocStatusStorage)
        await self.rag.initialize_storages()
        return self.rag
    
    def collect_files(self) -> List[Path]:
        """Collect files to index from repository"""
        repo_path = Path(self.config.lightrag_repo)
        
        # File patterns to include
        include_patterns = ['*.py', '*.md', '*.txt', '*.yaml', '*.yml', '*.json']
        
        # Directories to exclude
        exclude_dirs = {
            '.git', '__pycache__', '.pytest_cache', 'node_modules',
            '.venv', 'venv', '.env', 'build', 'dist', '*.egg-info'
        }
        
        files = []
        for pattern in include_patterns:
            for file_path in repo_path.rglob(pattern):
                # Skip if in excluded directory
                if any(excluded in file_path.parts for excluded in exclude_dirs):
                    continue
                    
                # Skip if too small
                if file_path.stat().st_size < self.config.min_file_size:
                    continue
                    
                files.append(file_path)
        
        return sorted(files)
    
    async def index_file(self, file_path: Path) -> bool:
        """Index a single file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Skip if content too small
            if len(content.strip()) < self.config.min_file_size:
                return False
            
            # Get relative path for better context
            rel_path = file_path.relative_to(self.config.lightrag_repo)
            
            # Add file context to content
            full_content = f"# File: {rel_path}\n\n{content}"
            
            await self.rag.ainsert(full_content)
            return True
            
        except Exception as e:
            print(f"   ✗ Error indexing {file_path.name}: {e}")
            return False
    
    async def index_repository(self) -> Tuple[int, int, int]:
        """Index entire repository
        
        Returns:
            Tuple of (indexed_count, skipped_count, error_count)
        """
        print("=" * 80)
        print("INDEXING REPOSITORY")
        print("=" * 80)
        
        # Initialize RAG
        await self.initialize_rag()
        
        # Collect files
        files_to_index = self.collect_files()
        
        # Index files
        indexed_count = 0
        skipped_count = 0
        error_count = 0
        
        for i, file_path in enumerate(files_to_index, 1):
            success = await self.index_file(file_path)
            
            if success:
                indexed_count += 1
            else:
                skipped_count += 1
            
            if i % self.config.batch_report_interval == 0:
                print(f"   ✓ Indexed {i}/{len(files_to_index)} files...")
        
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
