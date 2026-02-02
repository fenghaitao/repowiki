# Code Examples

### Home > API Reference > Code Examples

## Practical Code Examples for Using This Codebase

Here are 3 practical code examples demonstrating common real-world use cases of this codebase. Each example includes a clear title, code snippet, and explanation to help you understand its functionality.

---

### 1. **Generating a Hierarchical Wiki**

#### Code Snippet:
```python
from generator import WikiGenerator
from config import Config
import asyncio

async def generate_wiki():
    # Load configuration
    config = Config(repo_path="./my_repo", output_dir="./wiki_docs")
    generator = WikiGenerator(config, extended=True)

    # Generate the entire wiki
    await generator.generate_all()

# Run the generation process
asyncio.run(generate_wiki())
```

#### Explanation:
This example demonstrates how to use the `WikiGenerator` class to generate a hierarchical wiki from a code repository. The `Config` class is used to set the repository path and output directory. The `generate_all` method of the `WikiGenerator` creates the entire documentation, including category pages and a root index.

---

### 2. **Indexing a Repository**

#### Code Snippet:
```python
from indexer import RepositoryIndexer
from config import Config
import asyncio

async def index_repository():
    # Load configuration
    config = Config(repo_path="./my_repo", working_dir="./index_storage")
    indexer = RepositoryIndexer(config)

    # Index the repository
    indexed, skipped, errors = await indexer.index_repository()
    print(f"Indexed: {indexed}, Skipped: {skipped}, Errors: {errors}")

# Run the indexing process
asyncio.run(index_repository())
```

#### Explanation:
This example shows how to index a code repository using the `RepositoryIndexer` class. The `index_repository` method processes files in the repository and creates a knowledge graph for further use in documentation generation. The results include counts of indexed, skipped, and errored files.

---

### 3. **Testing the Setup**

#### Code Snippet:
```python
from config import Config
from cli import test_setup

def test_configuration():
    # Load configuration
    config = Config(repo_path="./my_repo")
    
    # Test the setup
    success = test_setup(config)
    if success:
        print("Setup is ready!")
    else:
        print("Setup encountered issues.")

test_configuration()
```

#### Explanation:
This example demonstrates how to test the setup of the codebase using the `test_setup` function. It validates the configuration, checks for dependencies, and ensures that the repository is ready for indexing and generation.

---

### 4. **Customizing Prompts for Documentation**

#### Code Snippet:
```python
from prompts import get_category_index_prompt

# Define a custom prompt for a new category
custom_prompt = get_category_index_prompt("Custom Category")
print("Custom Prompt:")
print(custom_prompt)
```

#### Explanation:
This example illustrates how to retrieve or define a custom prompt for generating an index page for a new category. The `get_category_index_prompt` function generates a structured prompt that can be used for creating detailed category documentation.

---

### 5. **Running Wiki Generation from CLI**

#### Code Snippet:
```bash
# Run the entire process (indexing + wiki generation) from the command line
python cli.py all --repo ./my_repo --output ./wiki_docs --extended
```

#### Explanation:
This command uses the CLI interface to index a repository and generate an extended hierarchical wiki. The `--extended` flag ensures that comprehensive documentation is generated, including additional categories and details.

---

These examples cover the most common workflows, including indexing, generating documentation, testing setup, and customizing prompts.

---

### References

- [1] prompts.py
- [2] generator.py
- [3] cli.py
- [4] indexer.py
- [6] config.py