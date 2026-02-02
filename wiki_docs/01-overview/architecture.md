# Architecture

### Home > Overview & Architecture > Architecture

#### 1. Overall Architecture Pattern

The codebase employs a **hierarchical architecture** for its structure, which is evident from its design to generate organized documentation from repositories. This pattern aligns well with the goal of creating clear, navigable, and modular documentation. The hierarchical design ensures scalability, allowing the system to handle various levels of complexity with ease. Additionally, this pattern supports parallel processing and modularity, making it efficient for large repositories.

The choice of this pattern stems from the need to structure documentation logically for developers and end-users. It simplifies navigation and ensures the generated wiki aligns with the natural hierarchy of the underlying codebase.

---

#### 2. Core Components

The primary components/modules of the codebase include:

- **Repository Indexer**:  
  This module indexes the code repository into a structured knowledge graph. It utilizes parallel batch processing to handle large repositories efficiently. The indexer collects files, reads their content, and integrates them into the knowledge graph using the LightRAG framework.

- **Wiki Generator**:  
  Responsible for generating hierarchical wiki documentation from the knowledge graph. It automates the creation of sections, pages, and navigation aids (e.g., breadcrumbs) to ensure a clear and accessible documentation structure.

- **Config Module**:  
  This module manages configuration settings, including repository paths, working directories, and API key integration. It ensures the proper initialization of the system and supports dynamic configurations for different setups.

These components interact through shared configurations and workflows. The **Repository Indexer** prepares the knowledge graph, which is then consumed by the **Wiki Generator** to produce the final output. The **Config Module** underpins both components, ensuring seamless operation.

---

#### 3. Data Flow

The data flow of the system can be summarized as follows:

1. **Input and Indexing**:
   - The process begins with the **Repository Indexer**, which collects files from the specified repository. Supported file types include Python scripts, Markdown files, and text files.
   - The contents of these files are read and processed into a knowledge graph using the LightRAG framework. This step involves embedding functions and parallel processing to optimize performance.

2. **Knowledge Graph Utilization**:
   - The knowledge graph serves as the central data structure, organizing the repository's content into a format suitable for generating documentation.

3. **Wiki Generation**:
   - The **Wiki Generator** consumes the knowledge graph to create structured documentation. Pages are generated in parallel, and a hierarchical navigation system (breadcrumbs, index pages) is created to ensure usability.

4. **Output**:
   - The final output is a hierarchical wiki, including a root index, section overviews, and detailed pages for each component or workflow.

**Main Entry Points**:
   - The **`RepositoryIndexer`** class initializes the indexing process, transforming the repository into a knowledge graph.
   - The **`WikiGenerator`** class processes the graph and generates the wiki documentation.

This structured approach ensures clarity, modularity, and scalability, making the system suitable for large and complex repositories.

### References

- [1] prompts.py
- [2] generator.py
- [3] indexer.py
- [4] cli.py