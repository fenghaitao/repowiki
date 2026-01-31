#!/usr/bin/env python3
"""
Master script to run the complete wiki generation process
"""
import asyncio
import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))

from importlib import import_module


async def main():
    print("\n" + "=" * 80)
    print("🚀 LIGHTRAG REPOSITORY WIKI GENERATION")
    print("=" * 80)
    print("""
This script will:
1. Index the LightRAG repository into a knowledge graph
2. Generate hierarchical wiki documentation

Estimated time: 30-60 minutes
Estimated cost: $10-20 in LLM API calls
""")
    
    response = input("\nProceed? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("❌ Cancelled")
        return
    
    # Step 1: Index repository
    print("\n" + "=" * 80)
    print("STEP 1: INDEXING REPOSITORY")
    print("=" * 80)
    
    try:
        # Import and run indexing
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "index_repo",
            Path(__file__).parent / "01_index_repository.py"
        )
        index_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(index_module)
        
        rag, working_dir = await index_module.index_repository()
        print("✅ Step 1 complete: Repository indexed")
        
    except Exception as e:
        print(f"❌ Error in Step 1: {e}")
        return
    
    # Small delay
    await asyncio.sleep(2)
    
    # Step 2: Generate wiki
    print("\n" + "=" * 80)
    print("STEP 2: GENERATING WIKI")
    print("=" * 80)
    
    try:
        # Import and run wiki generation
        spec = importlib.util.spec_from_file_location(
            "wiki_gen",
            Path(__file__).parent / "02_hierarchical_wiki_generator.py"
        )
        wiki_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(wiki_module)
        
        await wiki_module.main()
        print("✅ Step 2 complete: Wiki generated")
        
    except Exception as e:
        print(f"❌ Error in Step 2: {e}")
        return
    
    # Done
    print("\n" + "=" * 80)
    print("🎉 ALL DONE!")
    print("=" * 80)
    print(f"""
✅ Repository indexed
✅ Wiki generated

📂 Output location: {Path(__file__).parent / 'wiki_docs'}
📖 Open wiki_docs/README.md to start browsing

Next steps:
- Browse the wiki
- Review generated content
- Customize prompts if needed
- Set up automatic updates (git hooks)
""")


if __name__ == "__main__":
    asyncio.run(main())
