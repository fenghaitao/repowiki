"""
Repowiki: Hierarchical Wiki Generator for Code Repositories

A tool to generate comprehensive hierarchical wiki documentation
from code repositories using LightRAG knowledge graphs.

Uses GitHub Copilot models by default (same as adk-python/lightrag_openspec).
No authentication or API keys required - works out of the box!
"""

__version__ = "0.1.0"
__author__ = "LightRAG Contributors"

from .config import Config
from .indexer import RepositoryIndexer
from .generator import WikiGenerator

__all__ = [
    "Config",
    "RepositoryIndexer", 
    "WikiGenerator",
]
