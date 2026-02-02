"""Configuration for repowiki"""
import os
from pathlib import Path
from typing import Set, Optional
from dataclasses import dataclass, field


@dataclass
class Config:
    """Repowiki configuration"""
    
    # Paths
    repo_path: Path = Path(".")  # Current directory by default
    working_dir: Path = Path("./repowiki_storage")
    output_dir: Path = Path("./wiki_docs")
    workspace: str = "main"
    
    # Repository metadata (auto-detected from git if available)
    repo_name: Optional[str] = None  # Auto-detected from git or directory name
    
    # LLM settings - CHANGED: Use gpt-4o by default (128K context)
    llm_model_name: str = "github_copilot/gpt-4o"  # Changed from gpt-4o-mini
    embedding_model_name: str = "github_copilot/text-embedding-3-small"
    api_key: str = "oauth2"  # For GitHub Copilot
    
    # Indexing settings
    code_extensions: Set[str] = field(default_factory=lambda: {
        '.py', '.md', '.txt'
    })
    min_file_size: int = 50
    batch_report_interval: int = 10
    
    # Parallel processing settings (Ultra-aggressive - optimized for GitHub Copilot Business)
    # Pushing to 50-60% capacity utilization for maximum speed
    max_parallel_insert: int = 48      # Documents processed concurrently
    llm_model_max_async: int = 96      # Concurrent LLM calls
    embedding_func_max_async: int = 48  # Concurrent embedding calls
    
    @classmethod
    def from_env(cls, **overrides) -> "Config":
        """Create config from environment variables"""
        config_dict = {}
        
        if repo := os.getenv("REPO_PATH"):
            config_dict["repo_path"] = Path(repo)
        
        if working_dir := os.getenv("WORKING_DIR"):
            config_dict["working_dir"] = Path(working_dir)
        
        if output_dir := os.getenv("OUTPUT_DIR"):
            config_dict["output_dir"] = Path(output_dir)
        
        if workspace := os.getenv("WORKSPACE"):
            config_dict["workspace"] = workspace
        
        if repo_name := os.getenv("REPO_NAME"):
            config_dict["repo_name"] = repo_name
        
        if llm_model := os.getenv("LLM_MODEL"):
            config_dict["llm_model_name"] = llm_model
        
        if embed_model := os.getenv("EMBEDDING_MODEL"):
            config_dict["embedding_model_name"] = embed_model
        
        if api_key := os.getenv("API_KEY"):
            config_dict["api_key"] = api_key
        
        if min_size := os.getenv("MIN_FILE_SIZE"):
            config_dict["min_file_size"] = int(min_size)
        
        if batch := os.getenv("BATCH_REPORT_INTERVAL"):
            config_dict["batch_report_interval"] = int(batch)
        
        # Parallel processing settings
        if max_parallel := os.getenv("MAX_PARALLEL_INSERT"):
            config_dict["max_parallel_insert"] = int(max_parallel)
        
        if llm_async := os.getenv("LLM_MODEL_MAX_ASYNC"):
            config_dict["llm_model_max_async"] = int(llm_async)
        
        if embed_async := os.getenv("EMBEDDING_FUNC_MAX_ASYNC"):
            config_dict["embedding_func_max_async"] = int(embed_async)
        
        # Apply overrides
        config_dict.update(overrides)
        
        return cls(**config_dict)
    
    def validate(self):
        """Validate configuration"""
        if not self.repo_path.exists():
            raise ValueError(f"Repository path does not exist: {self.repo_path}")
        
        # Auto-detect repo name if not set
        if self.repo_name is None:
            self.repo_name = self._detect_repo_name()
        
        # Create output directory if it doesn't exist
        self.working_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _detect_repo_name(self) -> str:
        """Auto-detect repository name from git or directory name"""
        import subprocess
        
        # Try to get from git remote
        try:
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                url = result.stdout.strip()
                # Extract repo name from URL (e.g., https://github.com/user/repo.git -> repo)
                name = url.rstrip('/').split('/')[-1]
                if name.endswith('.git'):
                    name = name[:-4]
                return name
        except Exception:
            pass
        
        # Fallback to directory name
        return self.repo_path.resolve().name
