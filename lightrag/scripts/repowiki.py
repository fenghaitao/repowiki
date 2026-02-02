#!/usr/bin/env python3.12
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "lightrag-hku>=1.4.9,<2.0.0",
#     "openai>=1.0.0",
#     "tiktoken>=0.5.0",
#     "numpy>=1.24.0",
#     "networkx>=3.0.0",
#     "nano-vectordb>=0.0.4",
#     "python-dotenv>=1.0.0",
#     "llama-index-core>=0.10.0",
#     "llama-index-llms-litellm>=0.1.0",
#     "llama-index-embeddings-litellm>=0.1.0",
#     "litellm @ git+https://github.com/fenghaitao/litellm.git"
# ]
# ///
"""
LightRAG Wiki Generator - Generate comprehensive hierarchical documentation from code repositories
"""

import argparse
import asyncio
import os
import sys
import subprocess
from pathlib import Path
from typing import Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configuration
@dataclass
class Config:
    """LightRAG configuration"""
    
    # Paths
    repo_path: Path = Path(".")  # Current directory by default
    working_dir: Path = Path("./repowiki_storage")
    output_dir: Path = Path("./wiki_docs")
    workspace: str = "main"
    
    # Repository metadata (auto-detected from git if available)
    repo_name: Optional[str] = None  # Auto-detected from git or directory name
    
    # LLM settings - Use GitHub Copilot by default
    llm_model_name: str = "github_copilot/gpt-4o"
    embedding_model_name: str = "github_copilot/text-embedding-3-small"
    api_key: str = "oauth2"  # For GitHub Copilot
    
    # Indexing settings
    code_extensions: Set[str] = field(default_factory=lambda: {
        '.py', '.md', '.txt'
    })
    min_file_size: int = 50
    batch_report_interval: int = 10
    
    # Parallel processing settings (optimized for GitHub Copilot Business)
    max_parallel_insert: int = 48
    llm_model_max_async: int = 96
    embedding_func_max_async: int = 48
    
    @classmethod
    def from_env(cls, **overrides) -> "Config":
        """Create config from environment variables"""
        config_dict = {}
        
        if repo := os.getenv("REPO_PATH"):
            config_dict["repo_path"] = Path(repo)
        
        if working_dir := os.getenv("WORKING_DIR"):
            config_dict["working_dir"] = Path(working_dir)
        
        if output_dir := os.getenv("OUTPUT_DIR"):
            config_dict["output_dir"] = Path(output_dir)
        
        if workspace := os.getenv("WORKSPACE"):
            config_dict["workspace"] = workspace
        
        if repo_name := os.getenv("REPO_NAME"):
            config_dict["repo_name"] = repo_name
        
        if llm_model := os.getenv("LLM_MODEL"):
            config_dict["llm_model_name"] = llm_model
        
        if embed_model := os.getenv("EMBEDDING_MODEL"):
            config_dict["embedding_model_name"] = embed_model
        
        if api_key := os.getenv("API_KEY"):
            config_dict["api_key"] = api_key
        
        if min_size := os.getenv("MIN_FILE_SIZE"):
            config_dict["min_file_size"] = int(min_size)
        
        if batch := os.getenv("BATCH_REPORT_INTERVAL"):
            config_dict["batch_report_interval"] = int(batch)
        
        # Parallel processing settings
        if max_parallel := os.getenv("MAX_PARALLEL_INSERT"):
            config_dict["max_parallel_insert"] = int(max_parallel)
        
        if llm_async := os.getenv("LLM_MODEL_MAX_ASYNC"):
            config_dict["llm_model_max_async"] = int(llm_async)
        
        if embed_async := os.getenv("EMBEDDING_FUNC_MAX_ASYNC"):
            config_dict["embedding_func_max_async"] = int(embed_async)
        
        # Apply overrides
        config_dict.update(overrides)
        
        return cls(**config_dict)
    
    def validate(self):
        """Validate configuration"""
        if not self.repo_path.exists():
            raise ValueError(f"Repository path does not exist: {self.repo_path}")
        
        # Auto-detect repo name if not set
        if self.repo_name is None:
            self.repo_name = self._detect_repo_name()
        
        # Create output directory if it doesn't exist
        self.working_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _detect_repo_name(self) -> str:
        """Auto-detect repository name from git or directory name"""
        # Try to get from git remote
        try:
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                url = result.stdout.strip()
                # Extract repo name from URL
                name = url.rstrip('/').split('/')[-1]
                if name.endswith('.git'):
                    name = name[:-4]
                return name
        except Exception:
            pass
        
        # Fallback to directory name
        return self.repo_path.resolve().name


# Repository Indexer
class RepositoryIndexer:
    """Index repository into LightRAG knowledge graph"""
    
    def __init__(self, config: Config):
        self.config = config
        self.rag = None
    
    async def index_repository(self) -> Tuple[int, int, int]:
        """Index all files in repository"""
        import os
        from lightrag import LightRAG
        from lightrag.llm.llama_index_impl import (
            llama_index_complete_if_cache,
            llama_index_embed,
        )
        from lightrag.utils import EmbeddingFunc
        from llama_index.llms.litellm import LiteLLM
        from llama_index.embeddings.litellm import LiteLLMEmbedding
        
        # Set API key in environment
        os.environ["OPENAI_API_KEY"] = self.config.api_key
        
        print(f"\n📚 Indexing repository: {self.config.repo_name}")
        print(f"   Path: {self.config.repo_path}")
        print(f"   Working directory: {self.config.working_dir}")
        print(f"   LLM: {self.config.llm_model_name}")
        print(f"   Embedding: {self.config.embedding_model_name}")
        
        # Initialize LightRAG
        working_dir = str(self.config.working_dir / self.config.workspace)
        
        async def llm_model_func(
            prompt, system_prompt=None, history_messages=[], **kwargs
        ) -> str:
            if "llm_instance" not in kwargs:
                kwargs["llm_instance"] = LiteLLM(
                    model=self.config.llm_model_name,
                    api_key=self.config.api_key,
                    temperature=0.7,
                )
            return await llama_index_complete_if_cache(
                kwargs["llm_instance"], prompt, system_prompt, history_messages
            )
        
        async def embedding_func(texts: list[str]):
            embed_model = LiteLLMEmbedding(
                model_name=self.config.embedding_model_name,
                api_key=self.config.api_key,
            )
            return await llama_index_embed(texts, embed_model=embed_model)
        
        self.rag = LightRAG(
            working_dir=working_dir,
            workspace=self.config.workspace,
            llm_model_func=llm_model_func,
            embedding_func=EmbeddingFunc(
                embedding_dim=1536,
                max_token_size=8192,
                func=embedding_func
            ),
            llm_model_name=self.config.llm_model_name,
            max_parallel_insert=self.config.max_parallel_insert,
            llm_model_max_async=self.config.llm_model_max_async,
            embedding_func_max_async=self.config.embedding_func_max_async
        )
        await self.rag.initialize_storages()
        
        # Find all files
        files_to_index = []
        for ext in self.config.code_extensions:
            files_to_index.extend(self.config.repo_path.rglob(f"*{ext}"))
        
        # Filter by size and sort
        files_to_index = [
            f for f in files_to_index 
            if f.is_file() and f.stat().st_size >= self.config.min_file_size
        ]
        files_to_index.sort()
        
        print(f"\n📁 Found {len(files_to_index)} files to index")
        
        # Index files
        indexed = 0
        skipped = 0
        errors = 0
        
        for i, file_path in enumerate(files_to_index, 1):
            try:
                # Read file
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                
                if not content.strip():
                    skipped += 1
                    continue
                
                # Prepare document
                rel_path = file_path.relative_to(self.config.repo_path)
                doc = f"# File: {rel_path}\n\n{content}"
                
                # Insert into knowledge graph
                await self.rag.ainsert(doc)
                indexed += 1
                
                # Progress report
                if i % self.config.batch_report_interval == 0:
                    print(f"   Progress: {i}/{len(files_to_index)} files processed")
                
            except Exception as e:
                print(f"   ⚠️  Error indexing {file_path}: {e}")
                errors += 1
        
        print(f"\n✅ Indexing complete!")
        print(f"   Indexed: {indexed} files")
        print(f"   Skipped: {skipped} files (empty)")
        print(f"   Errors: {errors} files")
        
        return indexed, skipped, errors


# Wiki Generator
class WikiGenerator:
    """Generate hierarchical wiki from knowledge graph"""
    
    def __init__(self, config: Config, extended: bool = False):
        self.config = config
        self.extended = extended
        self.rag = None
    
    async def generate_all(self):
        """Generate complete wiki"""
        import os
        from lightrag import LightRAG
        from lightrag.llm.llama_index_impl import (
            llama_index_complete_if_cache,
            llama_index_embed,
        )
        from lightrag.utils import EmbeddingFunc
        from llama_index.llms.litellm import LiteLLM
        from llama_index.embeddings.litellm import LiteLLMEmbedding
        
        # Set API key in environment
        os.environ["OPENAI_API_KEY"] = self.config.api_key
        
        print(f"\n📖 Generating {'extended ' if self.extended else ''}wiki: {self.config.repo_name}")
        print(f"   Output directory: {self.config.output_dir}")
        
        # Initialize LightRAG
        working_dir = str(self.config.working_dir / self.config.workspace)
        
        async def llm_model_func(
            prompt, system_prompt=None, history_messages=[], **kwargs
        ) -> str:
            if "llm_instance" not in kwargs:
                kwargs["llm_instance"] = LiteLLM(
                    model=self.config.llm_model_name,
                    api_key=self.config.api_key,
                    temperature=0.7,
                )
            return await llama_index_complete_if_cache(
                kwargs["llm_instance"], prompt, system_prompt, history_messages
            )
        
        async def embedding_func(texts: list[str]):
            embed_model = LiteLLMEmbedding(
                model_name=self.config.embedding_model_name,
                api_key=self.config.api_key,
            )
            return await llama_index_embed(texts, embed_model=embed_model)
        
        self.rag = LightRAG(
            working_dir=working_dir,
            workspace=self.config.workspace,
            llm_model_func=llm_model_func,
            embedding_func=EmbeddingFunc(
                embedding_dim=1536,
                max_token_size=8192,
                func=embedding_func
            ),
            llm_model_name=self.config.llm_model_name,
            max_parallel_insert=self.config.max_parallel_insert,
            llm_model_max_async=self.config.llm_model_max_async,
            embedding_func_max_async=self.config.embedding_func_max_async
        )
        await self.rag.initialize_storages()
        
        # Generate pages
        if self.extended:
            await self._generate_extended()
        else:
            await self._generate_base()
        
        print(f"\n✅ Wiki generation complete!")
        print(f"   Output: {self.config.output_dir}")
        print(f"   Start: {self.config.output_dir}/README.md")
    
    async def _generate_base(self):
        """Generate base wiki structure"""
        await self._generate_home()
        await self._generate_overview()
    
    async def _generate_extended(self):
        """Generate extended wiki structure"""
        await self._generate_home()
        await self._generate_overview()
        await self._generate_getting_started()
        await self._generate_core_concepts()
        await self._generate_api_reference()
        await self._generate_development()
    
    async def _query(self, query: str, mode: str = "hybrid") -> str:
        """Query the knowledge graph"""
        from lightrag import QueryParam
        result = await self.rag.aquery(query, param=QueryParam(mode=mode))
        return result
    
    async def _generate_home(self):
        """Generate home page"""
        print("   📄 Generating README.md...")
        
        query = f"Provide a comprehensive overview of the {self.config.repo_name} project"
        content = await self._query(query, mode="hybrid")
        
        page = f"""# {self.config.repo_name}

{content}

## Documentation

- [Overview](01-overview/README.md) - Project overview and architecture
"""
        
        if self.extended:
            page += """- [Getting Started](02-getting-started/README.md) - Installation and setup
- [Core Concepts](03-core-concepts/README.md) - Key components and workflows
- [API Reference](04-api-reference/README.md) - API documentation
- [Development](05-development/README.md) - Contributing and development
"""
        
        (self.config.output_dir / "README.md").write_text(page)
    
    async def _generate_overview(self):
        """Generate overview section"""
        print("   📄 Generating 01-overview/...")
        
        section_dir = self.config.output_dir / "01-overview"
        section_dir.mkdir(exist_ok=True)
        
        # Section index
        index = f"""# Overview

- [Project Overview](project-overview.md)
- [Architecture](architecture.md)
- [Design Decisions](design-decisions.md)
"""
        (section_dir / "README.md").write_text(index)
        
        # Project overview
        query = f"What is {self.config.repo_name}? What problem does it solve?"
        content = await self._query(query, mode="global")
        (section_dir / "project-overview.md").write_text(f"# Project Overview\n\n{content}")
        
        # Architecture
        query = f"Describe the architecture and structure of {self.config.repo_name}"
        content = await self._query(query, mode="hybrid")
        (section_dir / "architecture.md").write_text(f"# Architecture\n\n{content}")
        
        # Design decisions
        query = f"What are the key design decisions in {self.config.repo_name}?"
        content = await self._query(query, mode="global")
        (section_dir / "design-decisions.md").write_text(f"# Design Decisions\n\n{content}")
    
    async def _generate_getting_started(self):
        """Generate getting started section"""
        print("   📄 Generating 02-getting-started/...")
        
        section_dir = self.config.output_dir / "02-getting-started"
        section_dir.mkdir(exist_ok=True)
        
        index = f"""# Getting Started

- [Installation](installation.md)
- [Configuration](configuration.md)
- [Quick Start](quick-start.md)
"""
        (section_dir / "README.md").write_text(index)
        
        # Installation
        query = f"How do I install and set up {self.config.repo_name}?"
        content = await self._query(query, mode="local")
        (section_dir / "installation.md").write_text(f"# Installation\n\n{content}")
        
        # Configuration
        query = f"How do I configure {self.config.repo_name}?"
        content = await self._query(query, mode="local")
        (section_dir / "configuration.md").write_text(f"# Configuration\n\n{content}")
        
        # Quick start
        query = f"Provide a quick start guide for {self.config.repo_name}"
        content = await self._query(query, mode="hybrid")
        (section_dir / "quick-start.md").write_text(f"# Quick Start\n\n{content}")
    
    async def _generate_core_concepts(self):
        """Generate core concepts section"""
        print("   📄 Generating 03-core-concepts/...")
        
        section_dir = self.config.output_dir / "03-core-concepts"
        section_dir.mkdir(exist_ok=True)
        
        index = f"""# Core Concepts

- [Key Components](key-components.md)
- [Workflows](workflows.md)
- [Data Models](data-models.md)
"""
        (section_dir / "README.md").write_text(index)
        
        # Key components
        query = f"What are the key components of {self.config.repo_name}?"
        content = await self._query(query, mode="hybrid")
        (section_dir / "key-components.md").write_text(f"# Key Components\n\n{content}")
        
        # Workflows
        query = f"Describe the main workflows in {self.config.repo_name}"
        content = await self._query(query, mode="hybrid")
        (section_dir / "workflows.md").write_text(f"# Workflows\n\n{content}")
        
        # Data models
        query = f"What are the data models and structures used in {self.config.repo_name}?"
        content = await self._query(query, mode="local")
        (section_dir / "data-models.md").write_text(f"# Data Models\n\n{content}")
    
    async def _generate_api_reference(self):
        """Generate API reference section"""
        print("   📄 Generating 04-api-reference/...")
        
        section_dir = self.config.output_dir / "04-api-reference"
        section_dir.mkdir(exist_ok=True)
        
        index = f"""# API Reference

- [Public API](public-api.md)
- [Classes](classes.md)
- [Functions](functions.md)
- [Examples](examples.md)
"""
        (section_dir / "README.md").write_text(index)
        
        # Public API
        query = f"Document the public API of {self.config.repo_name}"
        content = await self._query(query, mode="local")
        (section_dir / "public-api.md").write_text(f"# Public API\n\n{content}")
        
        # Classes
        query = f"List and describe the main classes in {self.config.repo_name}"
        content = await self._query(query, mode="local")
        (section_dir / "classes.md").write_text(f"# Classes\n\n{content}")
        
        # Functions
        query = f"List and describe the main functions in {self.config.repo_name}"
        content = await self._query(query, mode="local")
        (section_dir / "functions.md").write_text(f"# Functions\n\n{content}")
        
        # Examples
        query = f"Provide usage examples for {self.config.repo_name}"
        content = await self._query(query, mode="hybrid")
        (section_dir / "examples.md").write_text(f"# Examples\n\n{content}")
    
    async def _generate_development(self):
        """Generate development section"""
        print("   📄 Generating 05-development/...")
        
        section_dir = self.config.output_dir / "05-development"
        section_dir.mkdir(exist_ok=True)
        
        index = f"""# Development

- [Dependencies](dependencies.md)
- [Testing](testing.md)
- [Contributing](contributing.md)
- [Extensions](extensions.md)
"""
        (section_dir / "README.md").write_text(index)
        
        # Dependencies
        query = f"What are the dependencies of {self.config.repo_name}?"
        content = await self._query(query, mode="local")
        (section_dir / "dependencies.md").write_text(f"# Dependencies\n\n{content}")
        
        # Testing
        query = f"How do I test {self.config.repo_name}?"
        content = await self._query(query, mode="local")
        (section_dir / "testing.md").write_text(f"# Testing\n\n{content}")
        
        # Contributing
        query = f"How do I contribute to {self.config.repo_name}?"
        content = await self._query(query, mode="global")
        (section_dir / "contributing.md").write_text(f"# Contributing\n\n{content}")
        
        # Extensions
        query = f"How can I extend {self.config.repo_name}?"
        content = await self._query(query, mode="hybrid")
        (section_dir / "extensions.md").write_text(f"# Extensions\n\n{content}")


# CLI Functions
async def run_index(config: Config):
    """Run the indexing step"""
    print("\n" + "=" * 80)
    print("STEP 1: INDEXING REPOSITORY")
    print("=" * 80)
    
    indexer = RepositoryIndexer(config)
    indexed, skipped, errors = await indexer.index_repository()
    
    return indexed > 0


async def run_generate(config: Config, extended: bool = False):
    """Run the wiki generation step"""
    print("\n" + "=" * 80)
    mode_str = "EXTENDED " if extended else ""
    print(f"STEP 2: GENERATING {mode_str}WIKI")
    print("=" * 80)
    
    generator = WikiGenerator(config, extended=extended)
    await generator.generate_all()
    
    return True


async def run_all(config: Config, extended: bool = False):
    """Run both indexing and generation"""
    print("\n" + "=" * 80)
    print(f"🚀 {config.repo_name.upper()} REPOSITORY WIKI GENERATION")
    print("=" * 80)
    mode_str = "extended " if extended else ""
    print(f"""
This will:
1. Index the {config.repo_name} repository into a knowledge graph
2. Generate {mode_str}hierarchical wiki documentation

Estimated time: {'5-10' if extended else '2-3'} minutes
Cost: FREE (uses GitHub Copilot models)
""")
    
    response = input("\nProceed? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("❌ Cancelled")
        return False
    
    # Step 1: Index
    success = await run_index(config)
    if not success:
        print("❌ Indexing failed")
        return False
    
    # Small delay
    await asyncio.sleep(2)
    
    # Step 2: Generate
    success = await run_generate(config, extended=extended)
    if not success:
        print("❌ Wiki generation failed")
        return False
    
    # Done
    print("\n" + "=" * 80)
    print("🎉 ALL DONE!")
    print("=" * 80)
    print(f"""
✅ Repository indexed
✅ Wiki generated

📂 Output location: {config.output_dir}
📖 Open {config.output_dir}/README.md to start browsing

Next steps:
- Browse the wiki
- Review generated content
- Set up automatic updates (git hooks)
""")
    
    return True


def test_setup(config: Optional[Config] = None):
    """Test the setup"""
    if config is None:
        config = Config.from_env()
    
    # Validate config to trigger auto-detection
    try:
        config.validate()
    except Exception as e:
        pass
    
    print("=" * 80)
    print("TESTING SETUP")
    print("=" * 80)
    
    errors = []
    warnings = []
    
    # Check repository
    if config.repo_path.exists():
        print(f"✅ Repository found: {config.repo_path}")
        print(f"   Repository name: {config.repo_name}")
        
        py_files = list(config.repo_path.glob("**/*.py"))
        md_files = list(config.repo_path.glob("**/*.md"))
        print(f"   - Python files: {len(py_files)}")
        print(f"   - Markdown files: {len(md_files)}")
    else:
        errors.append(f"❌ Repository not found: {config.repo_path}")
    
    # Check Python version
    py_version = sys.version_info
    if py_version >= (3, 8):
        print(f"✅ Python version: {py_version.major}.{py_version.minor}.{py_version.micro}")
    else:
        errors.append(f"❌ Python 3.8+ required, found {py_version.major}.{py_version.minor}")
    
    # Try importing LightRAG
    try:
        import lightrag
        print("✅ LightRAG module can be imported")
    except ImportError as e:
        errors.append(f"❌ Cannot import LightRAG: {e}")
        warnings.append("⚠️  Install: uv pip install lightrag-hku")
    
    # Check write permissions
    try:
        config.working_dir.mkdir(exist_ok=True)
        config.output_dir.mkdir(exist_ok=True)
        test_file = config.working_dir / "test.txt"
        test_file.write_text("test")
        test_file.unlink()
        print("✅ Write permissions OK")
    except Exception as e:
        errors.append(f"❌ Write permission error: {e}")
    
    print("\n" + "=" * 80)
    if errors:
        print("ERRORS FOUND:")
        for error in errors:
            print(error)
    
    if warnings:
        print("\nWARNINGS:")
        for warning in warnings:
            print(warning)
    
    if not errors and not warnings:
        print("✅ ALL CHECKS PASSED - Ready to generate wiki!")
    elif not errors:
        print("⚠️  READY (with warnings)")
    else:
        print("❌ SETUP INCOMPLETE - Fix errors before proceeding")
    
    print("=" * 80)
    
    return len(errors) == 0


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Generate hierarchical wiki from code repository using LightRAG"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Index command
    index_parser = subparsers.add_parser("index", help="Index repository")
    index_parser.add_argument(
        "--repo",
        type=Path,
        help="Path to repository (default: current directory)"
    )
    index_parser.add_argument(
        "--working-dir",
        type=Path,
        help="Working directory for storage"
    )
    
    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate wiki")
    gen_parser.add_argument(
        "--working-dir",
        type=Path,
        help="Working directory with indexed data"
    )
    gen_parser.add_argument(
        "--output",
        type=Path,
        help="Output directory for wiki"
    )
    gen_parser.add_argument(
        "--extended",
        action="store_true",
        help="Generate extended wiki (~19 pages)"
    )
    gen_parser.add_argument(
        "--model",
        type=str,
        help="LLM model to use (default: github_copilot/gpt-4o)"
    )
    
    # All command
    all_parser = subparsers.add_parser("all", help="Run index and generate")
    all_parser.add_argument(
        "--repo",
        type=Path,
        help="Path to repository (default: current directory)"
    )
    all_parser.add_argument(
        "--extended",
        action="store_true",
        help="Generate extended wiki (~19 pages)"
    )
    all_parser.add_argument(
        "--model",
        type=str,
        help="LLM model to use (default: github_copilot/gpt-4o)"
    )
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Test setup")
    test_parser.add_argument(
        "--repo",
        type=Path,
        help="Path to repository (default: current directory)"
    )
    
    args = parser.parse_args()
    
    # Build config from args
    config_kwargs = {}
    if hasattr(args, 'repo') and args.repo:
        config_kwargs['repo_path'] = args.repo
    if hasattr(args, 'working_dir') and args.working_dir:
        config_kwargs['working_dir'] = args.working_dir
    if hasattr(args, 'output') and args.output:
        config_kwargs['output_dir'] = args.output
    if hasattr(args, 'model') and args.model:
        config_kwargs['llm_model_name'] = args.model
    
    config = Config.from_env(**config_kwargs)
    
    try:
        config.validate()
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        sys.exit(1)
    
    # Get extended flag
    extended = getattr(args, 'extended', False)
    
    # Run command
    if args.command == "index":
        asyncio.run(run_index(config))
    elif args.command == "generate":
        asyncio.run(run_generate(config, extended=extended))
    elif args.command == "all":
        asyncio.run(run_all(config, extended=extended))
    elif args.command == "test":
        success = test_setup(config)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
