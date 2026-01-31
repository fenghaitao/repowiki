#!/usr/bin/env python3
"""
Test script to verify setup before running full generation
"""
import sys
from pathlib import Path

def test_setup():
    print("=" * 80)
    print("TESTING SETUP")
    print("=" * 80)
    
    errors = []
    warnings = []
    
    # Check LightRAG repository exists
    lightrag_repo = Path(__file__).parent.parent / "LightRAG"
    if lightrag_repo.exists():
        print(f"✅ LightRAG repository found: {lightrag_repo}")
        
        # Count files
        py_files = list(lightrag_repo.glob("**/*.py"))
        md_files = list(lightrag_repo.glob("**/*.md"))
        print(f"   - Python files: {len(py_files)}")
        print(f"   - Markdown files: {len(md_files)}")
    else:
        errors.append(f"❌ LightRAG repository not found: {lightrag_repo}")
    
    # Check Python version
    py_version = sys.version_info
    if py_version >= (3, 8):
        print(f"✅ Python version: {py_version.major}.{py_version.minor}.{py_version.micro}")
    else:
        errors.append(f"❌ Python 3.8+ required, found {py_version.major}.{py_version.minor}")
    
    # Try importing LightRAG
    sys.path.insert(0, str(lightrag_repo))
    try:
        from lightrag import LightRAG
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
    test_dir = Path(__file__).parent / "test_write"
    try:
        test_dir.mkdir(exist_ok=True)
        test_file = test_dir / "test.txt"
        test_file.write_text("test")
        test_file.unlink()
        test_dir.rmdir()
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

if __name__ == "__main__":
    success = test_setup()
    sys.exit(0 if success else 1)
