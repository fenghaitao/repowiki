# Public API

### Home > API Reference > Public API

This page provides a detailed overview of the main public APIs available in the codebase. The focus is on APIs that external users are likely to interact with. Each API is organized by functionality and includes its purpose, key methods, parameters, return types, and usage examples.

---

#### **1. Repository Indexer API**
**Purpose:**  
The Repository Indexer API is responsible for indexing the contents of a code repository into a structured knowledge graph.

**Main Methods/Functions:**  
- `index_repository()`  
  - **Description:** Indexes the entire repository using parallel batch processing.  
  - **Parameters:** None.  
  - **Return Type:** A tuple containing:  
    - `indexed_count` (int): Number of successfully indexed files.  
    - `skipped_count` (int): Number of files that were skipped.  
    - `error_count` (int): Number of files that encountered errors.  

**Brief Usage Example:**  
```python
from indexer import RepositoryIndexer

indexer = RepositoryIndexer(config)
indexed_count, skipped_count, error_count = await indexer.index_repository()
```

---

#### **2. Wiki Generator API**
**Purpose:**  
The Wiki Generator API creates hierarchical wiki documentation from the indexed knowledge graph.

**Main Methods/Functions:**  
- `generate_all()`  
  - **Description:** Generates the entire wiki hierarchy, including categories, pages, and the root index.  
  - **Parameters:** None.  
  - **Return Type:** None.  

- `generate_page(title, prompt, mode, top_k, breadcrumb)`  
  - **Description:** Generates a single wiki page based on the provided title and prompt.  
  - **Parameters:**  
    - `title` (str): The title of the page.  
    - `prompt` (str): The prompt defining the content structure.  
    - `mode` (str): The mode for generation (e.g., "global", "local").  
    - `top_k` (int): The number of top results to consider.  
    - `breadcrumb` (str): The navigation breadcrumb.  
  - **Return Type:** A tuple containing the page title and generated content.  

**Brief Usage Example:**  
```python
from generator import WikiGenerator

generator = WikiGenerator(config)
await generator.generate_all()
```

---

#### **3. Configuration API**
**Purpose:**  
The Configuration API provides access to and validation of the settings required for indexing and generating the wiki.

**Main Methods/Functions:**  
- `from_env()`  
  - **Description:** Creates a configuration object from environment variables.  
  - **Parameters:**  
    - `**overrides`: Optional overrides for configuration values.  
  - **Return Type:** `Config` object.  

- `validate()`  
  - **Description:** Validates the configuration settings, ensuring paths exist and are ready for processing.  
  - **Parameters:** None.  
  - **Return Type:** None.  

**Brief Usage Example:**  
```python
from config import Config

config = Config.from_env()
config.validate()
```

---

#### **4. LightRAG Integration API**
**Purpose:**  
This API integrates the LightRAG framework for knowledge graph creation and querying.

**Main Methods/Functions:**  
- `initialize_rag()`  
  - **Description:** Initializes the LightRAG instance with the specified embedding and LLM functions.  
  - **Parameters:** None.  
  - **Return Type:** LightRAG instance.  

**Brief Usage Example:**  
```python
from generator import WikiGenerator

generator = WikiGenerator(config)
await generator.initialize_rag()
```

---

### References

- [1] prompts.py
- [2] generator.py
- [3] indexer.py
- [6] config.py