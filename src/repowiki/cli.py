"""Command-line interface for repowiki"""
import asyncio
import sys
from pathlib import Path
from typing import Optional

from .config import Config
from .indexer import RepositoryIndexer
from .generator import WikiGenerator


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
    print("🚀 LIGHTRAG REPOSITORY WIKI GENERATION")
    print("=" * 80)
    mode_str = "extended " if extended else ""
    print(f"""
This will:
1. Index the LightRAG repository into a knowledge graph
2. Generate {mode_str}hierarchical wiki documentation

Estimated time: {'60-90' if extended else '30-60'} minutes
Estimated cost: {'$20-40' if extended else '$10-20'} in LLM API calls
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
- Customize prompts if needed
- Set up automatic updates (git hooks)
""")
    
    return True


def test_setup(config: Optional[Config] = None):
    """Test the setup"""
    if config is None:
        config = Config.from_env()
    
    print("=" * 80)
    print("TESTING SETUP")
    print("=" * 80)
    
    errors = []
    warnings = []
    
    # Check LightRAG repository
    if config.lightrag_repo.exists():
        print(f"✅ LightRAG repository found: {config.lightrag_repo}")
        
        py_files = list(config.lightrag_repo.glob("**/*.py"))
        md_files = list(config.lightrag_repo.glob("**/*.md"))
        print(f"   - Python files: {len(py_files)}")
        print(f"   - Markdown files: {len(md_files)}")
    else:
        errors.append(f"❌ LightRAG repository not found: {config.lightrag_repo}")
    
    # Check Python version
    py_version = sys.version_info
    if py_version >= (3, 8):
        print(f"✅ Python version: {py_version.major}.{py_version.minor}.{py_version.micro}")
    else:
        errors.append(f"❌ Python 3.8+ required, found {py_version.major}.{py_version.minor}")
    
    # Try importing LightRAG
    sys.path.insert(0, str(config.lightrag_repo))
    try:
        import lightrag
        print("✅ LightRAG module can be imported")
    except ImportError as e:
        errors.append(f"❌ Cannot import LightRAG: {e}")
    
    # Check for OpenAI API key
    import os
    if os.environ.get("OPENAI_API_KEY"):
        print("✅ OPENAI_API_KEY is set")
    else:
        warnings.append("⚠️  OPENAI_API_KEY not set (required for generation)")
    
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
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate hierarchical wiki from code repository"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Index command
    index_parser = subparsers.add_parser("index", help="Index repository")
    index_parser.add_argument(
        "--repo",
        type=Path,
        help="Path to LightRAG repository"
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
        help="Generate extended wiki with comprehensive documentation"
    )
    gen_parser.add_argument(
        "--model",
        type=str,
        help="LLM model to use (e.g., gpt-4o, gpt-4o-mini)"
    )
    
    # All command
    all_parser = subparsers.add_parser("all", help="Run index and generate")
    all_parser.add_argument(
        "--repo",
        type=Path,
        help="Path to LightRAG repository"
    )
    all_parser.add_argument(
        "--extended",
        action="store_true",
        help="Generate extended wiki with comprehensive documentation"
    )
    all_parser.add_argument(
        "--model",
        type=str,
        help="LLM model to use (e.g., gpt-4o, gpt-4o-mini)"
    )
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Test setup")
    test_parser.add_argument(
        "--repo",
        type=Path,
        help="Path to LightRAG repository"
    )
    
    args = parser.parse_args()
    
    # Build config from args
    config_kwargs = {}
    if hasattr(args, 'repo') and args.repo:
        config_kwargs['lightrag_repo'] = args.repo
    if hasattr(args, 'working_dir') and args.working_dir:
        config_kwargs['working_dir'] = args.working_dir
    if hasattr(args, 'output') and args.output:
        config_kwargs['output_dir'] = args.output
    if hasattr(args, 'model') and args.model:
        config_kwargs['llm_model_name'] = args.model
    
    config = Config.from_env(**config_kwargs)
    
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
