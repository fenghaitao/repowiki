"""Tests for configuration"""
import pytest
from pathlib import Path
from repowiki.config import Config


def test_config_defaults():
    """Test default configuration"""
    config = Config()
    
    assert config.workspace == "main"
    assert config.min_file_size == 50
    assert '.py' in config.code_extensions


def test_config_custom():
    """Test custom configuration"""
    config = Config(
        lightrag_repo=Path("/custom/path"),
        workspace="test"
    )
    
    assert config.lightrag_repo == Path("/custom/path")
    assert config.workspace == "test"


def test_config_from_env(monkeypatch):
    """Test configuration from environment"""
    monkeypatch.setenv("LIGHTRAG_REPO", "/env/path")
    monkeypatch.setenv("LIGHTRAG_WORKING_DIR", "/env/working")
    
    config = Config.from_env()
    
    assert config.lightrag_repo == Path("/env/path")
    assert config.working_dir == Path("/env/working")
