# Project Structure

**BREADCRUMB: Home > Core Concepts > Project Structure**

# Project Structure

Understanding the directory and package structure of the codebase is essential for navigating and contributing effectively. Below is an overview of the main directories in the codebase, their purposes, and the types of files they contain:

## Main Directories

### 1. **`repowiki`**
   - **Purpose**: This is the primary application directory containing all core modules and classes for Repowiki.
   - **Files**: 
     - `config.py`: Handles configuration management, including paths, LLM settings, and parallel processing parameters.
     - `indexer.py`: Responsible for indexing the repository into a knowledge graph.
     - `generator.py`: Generates hierarchical wiki documentation using the indexed data.
     - `__init__.py`: Initializes the `repowiki` package and exports its main classes (`Config`, `RepositoryIndexer`, `WikiGenerator`).

### 2. **`tests`**
   - **Purpose**: Contains test cases for validating the functionality and reliability of the codebase.
   - **Files**: 
     - Test files for unit testing various components like the `Config`, `RepositoryIndexer`, and `WikiGenerator`.

### 3. **`scripts`**
   - **Purpose**: Includes utility scripts for setup, deployment, or maintenance tasks.
   - **Files**: 
     - Scripts for running the indexing or generation commands via the CLI.

### 4. **`docs`**
   - **Purpose**: Stores documentation files related to the project.
   - **Files**:
     - Markdown files (`*.md`) explaining various aspects of the project, such as installation, contributing guides, and architecture.

### 5. **`outputs`**
   - **Purpose**: Contains the generated hierarchical wiki documentation.
   - **Files**:
     - Generated `README.md` files for each category in the wiki.
     - Additional markdown files representing individual pages within the documentation.

### 6. **`storage`**
   - **Purpose**: Serves as a working directory for intermediate operations, such as storing indexed data.
   - **Files**:
     - Temporary files created during the indexing and generation processes.

### 7. **Root Directory**
   - **Purpose**: Contains high-level files for project management.
   - **Files**:
     - `README.md`: Provides an overview of the project.
     - `setup.py` or equivalent: Used for installation and packaging.
     - `.gitignore`: Specifies files and directories to ignore in version control.

This structured organization ensures that the codebase is modular, maintainable, and easy to navigate for developers.

### References

- [1] prompts.py
- [2] generator.py
- [4] indexer.py
- [5] __init__.py
- [6] config.py