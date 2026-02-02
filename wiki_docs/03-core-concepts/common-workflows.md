# Common Workflows

### Home > Core Concepts > Common Workflows

### Common Workflows

Below are two common workflows in this codebase that represent its core functionalities:

---

#### Workflow 1: **Indexing a Code Repository**
This workflow involves the process of organizing and storing the contents of a repository into a knowledge graph.

**Step-by-Step Process:**
1. **Initialize Configuration:**
   - Set the repository path, working directory, and other configurations using the `Config` class.
2. **Collect Files:**
   - Use the `RepositoryIndexer` class to gather all relevant files (e.g., `.py`, `.md`, `.txt`) from the repository while excluding hidden directories and unnecessary files.
3. **Read File Content:**
   - Read and prepare the content of each file for indexing. Files too small or with errors are skipped.
4. **Index Files:**
   - Use the `LightRAG` library to perform parallel batch processing of the files, creating embeddings and inserting them into the knowledge graph.
5. **Handle Errors:**
   - Any indexing errors are logged, and fallback mechanisms (individual processing) are triggered if batch processing fails.

**Components Involved:**
- `Config`: Handles configuration settings.
- `RepositoryIndexer`: Manages file collection and content preparation.
- `LightRAG`: Facilitates parallel batch processing and embedding creation.

---

#### Workflow 2: **Generating a Hierarchical Wiki**
This workflow describes how the indexed data is transformed into a structured wiki.

**Step-by-Step Process:**
1. **Initialize WikiGenerator:**
   - Configure the `WikiGenerator` class with necessary settings and validate configurations.
2. **Define Wiki Structure:**
   - Use predefined templates from `prompts.py` to define the hierarchical structure and content of the wiki pages.
3. **Generate Pages:**
   - For each section of the wiki (e.g., Core Concepts, API Reference), execute page generation tasks in parallel using prompts to query the knowledge graph.
4. **Create Category Indexes:**
   - Generate a `README.md` file for each category to provide an overview and table of contents.
5. **Generate Root Index:**
   - Create a root `README.md` file summarizing all sections and linking to category indexes.

**Components Involved:**
- `WikiGenerator`: Manages the generation of the entire hierarchical wiki.
- `prompts.py`: Provides prompt templates for generating content.
- `LightRAG`: Queries the knowledge graph for generating content.

---

These workflows ensure that the codebase is systematically indexed and documented, making it easier for developers to navigate and utilize its functionalities.

### References

- [1] prompts.py
- [2] generator.py
- [4] indexer.py