# Configuration Guide

```markdown
# Home > Getting Started > Configuration Guide

## Document Configuration Options

### 1. **Main Configuration**

#### Configuration File Format
The configuration for `repowiki` is defined in a Python class called `Config` (using the `dataclass` structure). This class provides a structured and programmatic approach to manage all configuration parameters.

#### Key Settings and Their Purpose
- **Paths**:
  - `repo_path`: Specifies the repository's path (default: `.`).
  - `working_dir`: Directory for storing intermediate files (default: `./repowiki_storage`).
  - `output_dir`: Directory for saving generated wiki documentation (default: `./wiki_docs`).
  - `workspace`: Specifies the workspace branch (default: `main`).

- **Repository Metadata**:
  - `repo_name`: The auto-detected repository name (default: None, falls back to directory name or Git remote).

- **LLM Settings**:
  - `llm_model_name`: Name of the large language model for processing (default: `github_copilot/gpt-4o`).
  - `embedding_model_name`: Model for embeddings (default: `github_copilot/text-embedding-3-small`).
  - `api_key`: API key for GitHub Copilot (default: `oauth2`).

- **Indexing Settings**:
  - `code_extensions`: File extensions to index (default: `.py`, `.md`, `.txt`).
  - `min_file_size`: Minimum file size to index (default: 50 bytes).
  - `batch_report_interval`: Interval for reporting batch progress (default: 10).

- **Parallel Processing Settings**:
  - `max_parallel_insert`: Maximum documents processed concurrently (default: 48).
  - `llm_model_max_async`: Maximum concurrent LLM calls (default: 96).
  - `embedding_func_max_async`: Maximum concurrent embedding calls (default: 48).

#### Default Values
Defaults are clearly defined in the `Config` class. These values ensure consistent behavior and can be overridden via environment variables or programmatically during initialization.

---

### 2. **Environment Variables**

#### Available Environment Variables
- `REPO_PATH`: Overrides `repo_path` to specify the repository location.
- `WORKING_DIR`: Overrides `working_dir` for intermediate operations.
- `OUTPUT_DIR`: Overrides `output_dir` to specify the output location.
- `WORKSPACE`: Overrides the default workspace branch.
- `REPO_NAME`: Manually specifies the repository name.
- `LLM_MODEL`: Overrides the default `llm_model_name`.
- `EMBEDDING_MODEL`: Overrides the embedding model name.
- `API_KEY`: Sets the API key for GitHub Copilot.
- `MIN_FILE_SIZE`: Overrides the `min_file_size` for indexing files.
- `BATCH_REPORT_INTERVAL`: Sets the interval for batch progress reporting.
- `MAX_PARALLEL_INSERT`: Configures the maximum parallel document insertion.
- `LLM_MODEL_MAX_ASYNC`: Customizes the maximum concurrent LLM calls.
- `EMBEDDING_FUNC_MAX_ASYNC`: Adjusts the maximum concurrent embedding calls.

#### How They Override Config
Values set in environment variables are read during runtime and take precedence over the default values in the `Config` class. The `Config.from_env()` method dynamically loads these variables, ensuring seamless integration with external environments.

---

### 3. **Advanced Configuration**

#### Performance Tuning Options
- **Parallel Processing**:
  - Adjust `max_parallel_insert`, `llm_model_max_async`, and `embedding_func_max_async` for optimal performance in high-capacity environments.
  - Example: Increase `max_parallel_insert` to 60 for faster document processing.

- **Batch Processing**:
  - Modify `batch_report_interval` to control reporting frequency during indexing.
  - Example: Set `batch_report_interval=5` for more frequent progress updates.

#### Custom Settings
- **Dynamic File Types**:
  - Extend `code_extensions` to include additional file types (e.g., `.json`, `.xml`).
  - Example:
    ```python
    config.code_extensions.update({'.json', '.xml'})
    ```

- **Custom Working Directory**:
  - Example:
    ```python
    os.environ['WORKING_DIR'] = '/custom/path'
    config = Config.from_env()
    ```

- **Model Selection**:
  - Switch to a different LLM or embedding model based on project requirements.
  - Example:
    ```python
    os.environ['LLM_MODEL'] = 'gpt-4o-mini'
    ```

---

### Examples
#### Example 1: Setting Up Configuration
```python
from repowiki.config import Config

config = Config.from_env()
config.validate()
```

#### Example 2: Overriding Defaults
```python
config = Config.from_env(
    repo_path='/my/repo',
    llm_model_name='gpt-4o-mini'
)
```

#### Example 3: Using Environment Variables
```bash
export REPO_PATH="/my/repo"
export LLM_MODEL="gpt-4o-mini"
python main.py
```
```