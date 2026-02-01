"""Configuration for repowiki"""
import os
from pathlib import Path
from typing import Set
from dataclasses import dataclass, field


@dataclass
class Config:
    """Repowiki configuration"""
    
    # Paths
    lightrag_repo: Path = Path("/home/hfeng1/lightrag")
    working_dir: Path = Path("./lightrag_storage")
    output_dir: Path = Path("./wiki_docs")
    workspace: str = "main"
    
    # LLM settings - CHANGED: Use gpt-4o by default (128K context)
    llm_model_name: str = "github_copilot/gpt-4o"  # Changed from gpt-4o-mini
    embedding_model_name: str = "github_copilot/text-embedding-3-small"
    api_key: str = "oauth2"  # For GitHub Copilot
    
    # Indexing settings
    code_extensions: Set[str] = field(default_factory=lambda: {
        '.py', '.md', '.txt', '.yaml', '.yml', '.json'
    })
    min_file_size: int = 50
    batch_report_interval: int = 10
    
    @classmethod
    def from_env(cls) -> "Config":
        """Create config from environment variables"""
        config_dict = {}
        
        if repo := os.getenv("LIGHTRAG_REPO"):
            config_dict["lightrag_repo"] = Path(repo)
        
        if working_dir := os.getenv("LIGHTRAG_WORKING_DIR"):
            config_dict["working_dir"] = Path(working_dir)
        
        if output_dir := os.getenv("LIGHTRAG_OUTPUT_DIR"):
            config_dict["output_dir"] = Path(output_dir)
        
        if workspace := os.getenv("WORKSPACE"):
            config_dict["workspace"] = workspace
        
        if llm_model := os.getenv("LIGHTRAG_LLM_MODEL"):
            config_dict["llm_model_name"] = llm_model
        
        if embed_model := os.getenv("LIGHTRAG_EMBEDDING_MODEL"):
            config_dict["embedding_model_name"] = embed_model
        
        if api_key := os.getenv("LIGHTRAG_API_KEY"):
            config_dict["api_key"] = api_key
        
        if min_size := os.getenv("MIN_FILE_SIZE"):
            config_dict["min_file_size"] = int(min_size)
        
        if batch := os.getenv("BATCH_REPORT_INTERVAL"):
            config_dict["batch_report_interval"] = int(batch)
        
        return cls(**config_dict)
    
    def validate(self):
        """Validate configuration"""
        if not self.lightrag_repo.exists():
            raise ValueError(f"Repository path does not exist: {self.lightrag_repo}")
        
        # Create output directory if it doesn't exist
        self.working_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
