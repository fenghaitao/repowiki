# Getting Started

### Home > Getting Started > Getting Started

# Getting Started

Welcome to the **Getting Started** guide for this project! This section provides step-by-step instructions to help you install, configure, and begin using the codebase effectively. Follow the instructions below to set up your environment and explore the project's capabilities.

---

## 1. Installation

### Prerequisites
Before you begin, ensure that you have the following tools and versions installed on your system:
- **Programming Language**: Python 3.8 or higher
- **Package Manager**: pip (comes with Python)
- **Version Control**: Git (for cloning the repository)
- **Other Tools**: Ensure `lightrag` and `GitHub Copilot` models are accessible for the project.

### Installation Steps
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```
2. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Environment Setup
- Ensure the `OPENAI_API_KEY` environment variable is set for using AI-powered features (e.g., LLM integration). You can set it as follows:
  ```bash
  export OPENAI_API_KEY=your_api_key
  ```
- Confirm that the `lightrag` module is installed:
  ```bash
  pip install lightrag
  ```
- Verify the setup:
  ```bash
  python -m repowiki.cli test --repo <path_to_repo>
  ```

---

## 2. Basic Usage

### Simplest Way to Use the Project
The primary way to interact with this project is through the command-line interface (CLI). You can start by generating a wiki from your code repository.

1. **Index the Repository**:
   ```bash
   python -m repowiki.cli index --repo <path_to_repo>
   ```
2. **Generate the Wiki**:
   ```bash
   python -m repowiki.cli generate --working-dir <working_directory> --output <output_directory>
   ```

### First Example
To create an extended wiki with comprehensive documentation:
```bash
python -m repowiki.cli all --repo <path_to_repo> --extended
```

### Expected Output
- The generated wiki documentation will be saved in the specified output directory (`<output_directory>`).
- Open the `README.md` file in the output directory to explore the documentation.

---

## 3. Configuration

### Required Configuration
The project uses a `Config` class to manage various settings. Key configurations include:
- `repo_path`: Path to the repository to be indexed.
- `working_dir`: Directory for temporary storage during processing.
- `output_dir`: Directory where the generated documentation will be saved.

### Common Settings
- **Parallel Processing**:
  - `max_parallel_insert`: Number of documents processed concurrently.
  - `llm_model_max_async`: Maximum concurrent API calls to the LLM.
- **File Types**:
  - Specify file types to index (e.g., `.py`, `.md`, `.txt`) using the `code_extensions` setting.
- **Minimum File Size**:
  - Set the `min_file_size` to exclude small files from indexing.

To override these settings, you can use environment variables or pass parameters via the CLI. For example:
```bash
export REPO_PATH=/path/to/repo
export OUTPUT_DIR=/path/to/output
```

---

Follow these steps to get started with the project. If you encounter any issues, refer to the [FAQ](../06-troubleshooting/faq.md) section for troubleshooting tips.

---

*Generated using LightRAG with GitHub Copilot models.* 

### References

- [2] prompts.py
- [3] cli.py
- [6] config.py