"""Configuration management for repowiki"""
from pathlib import Path
from typing import Set, Optional
from dataclasses import dataclass, field


@dataclass
class Config:
    """Configuration for repowiki"""
    
    # Paths
    lightrag_repo: Path = Path("/home/hfeng1/lightrag")
    working_dir: Path = Path("lightrag_storage")
    output_dir: Path = Path("wiki_docs")
    workspace: str = "main"
    
    # LLM Configuration (defaults to GitHub Copilot - same as lightrag_openspec)
    llm_model_name: str = "github_copilot/gpt-4o-mini"
    embedding_model_name: str = "github_copilot/text-embedding-3-small"
    api_key: str = "oauth2"  # For GitHub Copilot
    
    # Indexing settings
    code_extensions: Set[str] = field(default_factory=lambda: {
        '.py', '.md', '.yaml', '.yml', '.json', '.txt', '.toml'
    })
    
    skip_dirs: Set[str] = field(default_factory=lambda: {
        '__pycache__', '.git', '.pytest_cache', 'node_modules',
        '.venv', 'venv', 'env', '.eggs', '*.egg-info',
        'build', 'dist', '.tox', 'htmlcov', '.mypy_cache',
        'lightrag_webui', 'assets', 'examples/unofficial-sample'
    })
    
    # Processing settings
    min_file_size: int = 50  # Minimum characters to index
    batch_report_interval: int = 10  # Report progress every N files
    chunk_token_size: int = 1200
    chunk_overlap_token_size: int = 100
    
    @classmethod
    def from_env(cls, **kwargs) -> "Config":
        """Create config from environment variables and overrides"""
        import os
        
        config_dict = {}
        
        # Check for environment variables
        if repo_path := os.getenv("LIGHTRAG_REPO"):
            config_dict["lightrag_repo"] = Path(repo_path)
        
        if working := os.getenv("LIGHTRAG_WORKING_DIR"):
            config_dict["working_dir"] = Path(working)
        
        if output := os.getenv("LIGHTRAG_OUTPUT_DIR"):
            config_dict["output_dir"] = Path(output)
        
        if llm_model := os.getenv("LIGHTRAG_LLM_MODEL"):
            config_dict["llm_model_name"] = llm_model
        
        if embed_model := os.getenv("LIGHTRAG_EMBEDDING_MODEL"):
            config_dict["embedding_model_name"] = embed_model
        
        if api_key := os.getenv("LIGHTRAG_API_KEY"):
            config_dict["api_key"] = api_key
        
        # Override with kwargs
        config_dict.update(kwargs)
        
        return cls(**config_dict)
    
    def validate(self) -> bool:
        """Validate configuration"""
        if not self.lightrag_repo.exists():
            raise ValueError(f"LightRAG repository not found: {self.lightrag_repo}")
        
        # Create directories if needed
        self.working_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        return True
