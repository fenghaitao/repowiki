"""Integration tests for wiki generator"""
import pytest
from pathlib import Path
from repowiki.config import Config


def test_generator_config():
    """Test generator can be configured"""
    config = Config()
    assert config.workspace == "main"


def test_generator_extended_config():
    """Test generator extended mode configuration"""
    config = Config()
    # Extended mode is passed to WikiGenerator constructor
    # This test just verifies config works
    assert config.llm_model_name is not None
