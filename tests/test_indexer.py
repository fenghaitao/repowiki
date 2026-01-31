"""Tests for repository indexer"""
import pytest
from pathlib import Path
from repowiki.config import Config
from repowiki.indexer import RepositoryIndexer


def test_indexer_init():
    """Test indexer initialization"""
    config = Config(lightrag_repo=Path("/tmp"))
    indexer = RepositoryIndexer(config)
    
    assert indexer.config == config
    assert indexer.rag is None


def test_collect_files(tmp_path):
    """Test file collection"""
    # Create test files
    (tmp_path / "test.py").write_text("print('hello')")
    (tmp_path / "test.md").write_text("# Hello")
    (tmp_path / "test.txt").write_text("text")
    (tmp_path / "ignore.log").write_text("log")
    
    config = Config(
        lightrag_repo=tmp_path,
        code_extensions={'.py', '.md', '.txt'}
    )
    indexer = RepositoryIndexer(config)
    
    files = indexer.collect_files()
    
    assert len(files) == 3
    assert any(f.name == "test.py" for f in files)
    assert any(f.name == "test.md" for f in files)
    assert any(f.name == "test.txt" for f in files)
    assert not any(f.name == "ignore.log" for f in files)
