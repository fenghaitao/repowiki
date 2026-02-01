"""Tests for repository indexer"""
import pytest
from pathlib import Path
from repowiki.config import Config


def test_indexer_config():
    """Test indexer configuration"""
    config = Config(lightrag_repo=Path("/tmp"))
    assert config.lightrag_repo == Path("/tmp")


def test_file_collection_config(tmp_path):
    """Test file collection configuration"""
    # Create test files
    (tmp_path / "test.py").write_text("print('hello')")
    (tmp_path / "test.md").write_text("# Hello")
    (tmp_path / "test.txt").write_text("text")
    (tmp_path / "ignore.log").write_text("log")
    
    config = Config(
        lightrag_repo=tmp_path,
        code_extensions={'.py', '.md', '.txt'}
    )
    
    # Verify config
    assert config.lightrag_repo == tmp_path
    assert '.py' in config.code_extensions
    assert '.md' in config.code_extensions
    assert '.txt' in config.code_extensions
