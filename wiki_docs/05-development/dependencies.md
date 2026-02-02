# Dependencies

**Home > Development Guide > Dependencies**

# Dependencies

This section provides an analysis of the external dependencies and system requirements for the codebase.

---

## 1. External Dependencies

### Major Libraries/Packages Used:
- **LightRAG**: A framework used for building knowledge graphs, supporting LLM functionalities and embeddings. It is critical for repository indexing and wiki generation.
- **GitHub Copilot Models**: Provides AI-powered coding assistance, used for text generation and embedding within the documentation process.
- **LiteLLM**: A lightweight language model implementation integrated for generating embeddings and text completions.
- **llama_index**: Used for managing LLM queries and embeddings in conjunction with the LiteLLM library.

### Purpose of Each Major Dependency:
- **LightRAG**: Facilitates batch insertions with automatic parallelization, enabling efficient knowledge graph creation.
- **GitHub Copilot Models**: Powers the AI-based code completion, enhancing the documentation generation process.
- **LiteLLM**: Provides optimized operations for language models, ensuring seamless integration with the documentation workflow.
- **llama_index**: Handles embedding and query functions, enabling robust and scalable documentation generation.

---

## 2. System Requirements

### Platform Requirements (OS, Runtime):
- **Operating System**: Compatible with Unix-based systems (Linux, macOS) and Windows.
- **Runtime**: Python version **3.8 or higher** is required.

### Minimum Versions (if critical):
- **Python**: 3.8+ (critical for compatibility with libraries and frameworks used).
- **LightRAG**: Latest version recommended for full functionality.
- **GitHub Copilot Models**: Requires a valid API key and access to the latest model versions.

---

### References

- [1] generator.py
- [2] prompts.py
- [4] indexer.py
- [6] __init__.py