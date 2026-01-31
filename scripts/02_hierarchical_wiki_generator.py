#!/usr/bin/env python3
"""
Step 2: Generate hierarchical wiki from the knowledge graph
"""
import os
import sys
import asyncio
from pathlib import Path
from typing import Dict, List, Tuple

# Add LightRAG to path
LIGHTRAG_REPO = Path(__file__).parent.parent / "LightRAG"
sys.path.insert(0, str(LIGHTRAG_REPO))

from lightrag import LightRAG, QueryParam
from lightrag.llm import openai_complete_if_cache, openai_embedding


class HierarchicalWikiGenerator:
    """Generates hierarchical wiki documentation from knowledge graph"""
    
    def __init__(self, working_dir: str, workspace: str, output_dir: str):
        self.rag = LightRAG(
            working_dir=working_dir,
            workspace=workspace,
            llm_model_func=openai_complete_if_cache,
            embedding_func=openai_embedding
        )
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.structure = self._define_hierarchy()
        self.generated_pages = []
    
    def _define_hierarchy(self) -> Dict:
        """Define the hierarchical wiki structure"""
        return {
            "01-overview": {
                "title": "Overview & Architecture",
                "pages": [
                    {
                        "name": "project-overview",
                        "title": "Project Overview",
                        "mode": "global",
                        "top_k": 100,
                        "prompt": """
Given this LightRAG codebase, create a comprehensive Project Overview:

1. **Purpose & Goals**
   - What does LightRAG do?
   - What problems does it solve?
   - Who is the target audience?

2. **Core Features**
   - List main features (entity extraction, graph construction, query modes)
   - Unique aspects compared to other RAG frameworks
   - Notable integrations

3. **Technology Stack**
   - Programming languages used
   - Key frameworks and libraries
   - Database systems supported
   - External services/APIs

4. **Project Structure**
   - High-level directory organization
   - Main components/modules
   - How they interact

Format as markdown with clear sections and bullet points.
"""
                    },
                    {
                        "name": "architecture",
                        "title": "Architecture",
                        "mode": "global",
                        "top_k": 100,
                        "prompt": """
Describe the LightRAG system architecture for visualization:

1. **System Components**
   - Identify all major components (LightRAG core, storage backends, LLM integration, API server)
   - Describe responsibility of each component

2. **Component Relationships**
   - How components communicate
   - Main data flows
   - Which components depend on which

3. **Storage Architecture**
   - Graph storage options (NetworkX, Neo4j, Memgraph, etc.)
   - Vector storage options (Milvus, Qdrant, FAISS, etc.)
   - KV storage options (JSON, MongoDB, Redis, etc.)

4. **Architectural Patterns**
   - Pluggable storage backends
   - Async processing
   - Cache-driven rebuilding

Provide structured output with:
- Component names and descriptions
- Directional relationships (A → B)
- Layer hierarchy

Format as markdown that can be used to generate a diagram.
"""
                    },
                    {
                        "name": "design-decisions",
                        "title": "Design Decisions",
                        "mode": "global",
                        "top_k": 100,
                        "prompt": """
Identify key design decisions in LightRAG:

1. **Architectural Choices**
   - Why flat entity-relation graph instead of hierarchical communities?
   - Trade-offs made (speed vs sophistication)
   - Problems solved

2. **Technology Choices**
   - Why these specific frameworks/libraries?
   - Why support 12+ storage backends?
   - Why async/await design?

3. **Code Organization**
   - Structure principles
   - Conventions
   - Module separation

4. **Scalability & Performance**
   - How system scales
   - Performance considerations
   - Caching strategies

5. **Developer Experience**
   - Why simple API?
   - Why incremental updates?
   - Why multi-workspace support?

Present as "Design Decisions" document explaining rationale.
"""
                    }
                ]
            },
            "02-modules": {
                "title": "Modules",
                "index_prompt": """
Create a comprehensive Module Index for LightRAG:

1. **Module Overview**
   High-level description of how modules are organized

2. **Module Hierarchy**
   Show parent-child relationships in tree format:
   ```
   Core
   ├─ lightrag.py (orchestrator)
   ├─ operate.py (operations)
   └─ base.py (storage abstractions)
   
   Storage (kg/)
   ├─ Graph backends
   ├─ Vector backends
   └─ KV backends
   
   LLM Integration (llm/)
   ├─ OpenAI
   ├─ Ollama
   └─ Other providers
   
   API (api/)
   └─ REST server
   ```

3. **Module Quick Reference**
   Table with: Module, Purpose, Dependencies, LOC, Complexity

4. **Navigation**
   Links to each module's detailed documentation

Format as module map with ASCII tree.
""",
                "subfolders": {
                    "core": {
                        "pages": [
                            {
                                "name": "lightrag-orchestrator",
                                "title": "LightRAG Orchestrator",
                                "mode": "local",
                                "top_k": 80,
                                "prompt": """
Document the lightrag.py module (LightRAG class):

1. **Purpose**: Main orchestrator class
2. **Key Components**: LightRAG class, QueryParam class
3. **Public API**: 
   - __init__ parameters (~67 configuration options)
   - ainsert() method
   - aquery() method
   - adelete methods
4. **Configuration**: All initialization parameters with descriptions
5. **Usage Examples**: Basic initialization, document insertion, querying
6. **Query Modes**: local, global, hybrid, naive, mix
7. **Performance**: Token management, async processing

Format as comprehensive module documentation.
"""
                            },
                            {
                                "name": "operate-module",
                                "title": "Operations Module",
                                "mode": "local",
                                "top_k": 80,
                                "prompt": """
Document the operate.py module:

1. **Purpose**: Core operations for entity extraction, graph construction
2. **Key Functions**:
   - chunking_by_token_size()
   - extract_entities()
   - merge_nodes_and_edges()
   - kg_query()
   - naive_query()
3. **Entity Extraction**: How LLM extracts entities and relationships
4. **Graph Construction**: How entities are merged and stored
5. **Query Processing**: How different query modes work
6. **Examples**: Code snippets for key operations

Format as detailed API reference.
"""
                            },
                            {
                                "name": "storage-base",
                                "title": "Storage Abstractions",
                                "mode": "local",
                                "top_k": 60,
                                "prompt": """
Document the base.py storage abstractions:

1. **Purpose**: Define storage interfaces
2. **Storage Classes**:
   - BaseKVStorage: Key-value storage interface
   - BaseVectorStorage: Vector embedding storage interface
   - BaseGraphStorage: Graph storage interface
   - DocStatusStorage: Document status tracking
3. **Methods**: Required methods for each interface
4. **Implementation Guide**: How to create custom storage backend
5. **Examples**: Reference implementations

Format as API documentation with interface definitions.
"""
                            }
                        ]
                    },
                    "storage": {
                        "pages": [
                            {
                                "name": "storage-overview",
                                "title": "Storage Backends Overview",
                                "mode": "mix",
                                "top_k": 100,
                                "prompt": """
Document all storage backend options in LightRAG:

1. **Graph Storage**:
   - NetworkX (default, in-memory)
   - Neo4j (production)
   - Memgraph
   - PostgreSQL AGE

2. **Vector Storage**:
   - NanoVectorDB (default, lightweight)
   - Milvus
   - Qdrant
   - FAISS
   - Redis

3. **KV Storage**:
   - JSON (default)
   - MongoDB
   - Redis
   - PostgreSQL

4. **Selection Guide**: When to use each backend
5. **Configuration**: How to configure different backends
6. **Performance**: Comparison of different options

Format as comprehensive storage guide with comparison table.
"""
                            }
                        ]
                    },
                    "llm": {
                        "pages": [
                            {
                                "name": "llm-integration",
                                "title": "LLM Integration",
                                "mode": "local",
                                "top_k": 80,
                                "prompt": """
Document LLM integration in LightRAG:

1. **Supported Providers**:
   - OpenAI (openai.py)
   - Azure OpenAI (azure_openai.py)
   - Ollama (ollama.py)
   - Gemini (gemini.py)
   - Anthropic (anthropic.py)
   - Hugging Face (hf.py)
   - Others

2. **Configuration**: How to configure each provider
3. **Custom LLM**: How to add custom LLM provider
4. **Caching**: LLM response caching mechanism
5. **Examples**: Code for each provider

Format as integration guide with code examples.
"""
                            }
                        ]
                    },
                    "api": {
                        "pages": [
                            {
                                "name": "rest-api",
                                "title": "REST API Server",
                                "mode": "local",
                                "top_k": 80,
                                "prompt": """
Document the FastAPI server (lightrag/api/):

1. **Server Overview**: FastAPI-based REST API
2. **Endpoints**:
   - Document routes (upload, delete, status)
   - Query routes (query, context retrieval)
   - Graph routes (visualization, node/edge management)
   - Ollama compatibility routes
3. **Authentication**: How auth works
4. **Configuration**: Server configuration options
5. **Deployment**: How to deploy with Gunicorn
6. **Examples**: cURL examples for each endpoint

Format as API reference documentation.
"""
                            }
                        ]
                    }
                }
            },
            "03-guides": {
                "title": "Guides",
                "pages": [
                    {
                        "name": "getting-started",
                        "title": "Getting Started",
                        "mode": "hybrid",
                        "top_k": 100,
                        "prompt": """
Create comprehensive Getting Started guide for LightRAG:

1. **Prerequisites**: Python version, system requirements
2. **Installation**:
   - pip install lightrag
   - From source
3. **Quick Start**:
   - Initialize LightRAG
   - Insert documents
   - Query the knowledge graph
4. **Configuration**: Basic configuration options
5. **First Steps Tutorial**: Walk through simple example
6. **Next Steps**: Links to advanced topics

Format as friendly step-by-step guide with code examples.
"""
                    },
                    {
                        "name": "configuration",
                        "title": "Configuration Guide",
                        "mode": "local",
                        "top_k": 80,
                        "prompt": """
Document all LightRAG configuration options:

1. **LightRAG Parameters**:
   - working_dir
   - workspace
   - llm_model_func
   - embedding_func
   - Storage backend options
   - Token limits
   - Async settings

2. **Environment Variables**:
   - OPENAI_API_KEY
   - Storage connection strings
   - Other env vars

3. **Configuration Patterns**:
   - Local development
   - Production deployment
   - Different storage backends

4. **Examples**: Configuration for common scenarios

Format as configuration reference with examples.
"""
                    }
                ]
            },
            "04-api-reference": {
                "title": "API Reference",
                "pages": [
                    {
                        "name": "quick-start",
                        "title": "API Quick Start",
                        "mode": "hybrid",
                        "top_k": 60,
                        "prompt": """
Create API quick start guide:

1. **Starting the Server**: How to run lightrag-server
2. **Authentication**: Setting up API keys
3. **Basic Operations**:
   - Upload document
   - Query
   - Check status
4. **Examples**: cURL examples for common operations

Format as quick reference guide.
"""
                    }
                ]
            },
            "05-development": {
                "title": "Development",
                "pages": [
                    {
                        "name": "testing",
                        "title": "Testing Guide",
                        "mode": "local",
                        "top_k": 80,
                        "prompt": """
Document testing in LightRAG:

1. **Test Structure**: tests/ directory organization
2. **Running Tests**: pytest commands
3. **Test Types**: Unit, integration, offline tests
4. **Test Markers**: offline, integration, requires_db
5. **Writing Tests**: Best practices
6. **CI/CD**: GitHub Actions workflow

Format as testing documentation.
"""
                    },
                    {
                        "name": "contributing",
                        "title": "Contributing Guide",
                        "mode": "hybrid",
                        "top_k": 80,
                        "prompt": """
Create contributing guide:

1. **Getting Started**: Fork, clone, setup
2. **Development Workflow**: Branching, commits, PRs
3. **Code Standards**: Style guide, linting (ruff)
4. **Testing Requirements**: Coverage, CI checks
5. **Documentation**: How to update docs
6. **Review Process**: What happens after PR submission

Format as CONTRIBUTING.md style guide.
"""
                    }
                ]
            },
            "06-troubleshooting": {
                "title": "Troubleshooting",
                "pages": [
                    {
                        "name": "faq",
                        "title": "FAQ",
                        "mode": "hybrid",
                        "top_k": 100,
                        "prompt": """
Generate FAQ for LightRAG:

**General**:
- What is LightRAG?
- How is it different from GraphRAG?
- What are the main features?

**Installation**:
- Installation requirements?
- Common installation issues?

**Usage**:
- How to choose query mode?
- How to select storage backend?
- How to handle large documents?

**Performance**:
- How to optimize performance?
- What are the token limits?
- How does caching work?

20-30 questions total with concise answers.
Format as FAQ document.
"""
                    },
                    {
                        "name": "common-issues",
                        "title": "Common Issues",
                        "mode": "naive",
                        "top_k": 80,
                        "prompt": """
Document common issues and solutions:

1. **Installation Issues**:
   - Dependency conflicts
   - Version incompatibilities

2. **Runtime Errors**:
   - Connection errors
   - Memory issues
   - Token limit exceeded

3. **Performance Issues**:
   - Slow queries
   - High memory usage

For each: Problem, Symptoms, Cause, Solution

Format as troubleshooting guide.
"""
                    }
                ]
            }
        }
    
    async def generate_section(
        self,
        title: str,
        prompt: str,
        mode: str = "global",
        top_k: int = 60,
        breadcrumb: str = ""
    ) -> Tuple[str, str]:
        """Generate a single wiki section"""
        print(f"📝 Generating: {title}...")
        
        try:
            # Add breadcrumb to prompt
            enhanced_prompt = f"BREADCRUMB: {breadcrumb}\n\n{prompt}\n\nInclude breadcrumb at the top."
            
            result = await self.rag.aquery(
                enhanced_prompt,
                param=QueryParam(
                    mode=mode,
                    top_k=top_k,
                    only_need_context=False
                )
            )
            
            print(f"✅ Generated: {title}")
            return (title, result)
            
        except Exception as e:
            print(f"❌ Error generating {title}: {e}")
            return (title, None)
    
    def _write_file(self, path: Path, content: str):
        """Write content to file"""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    async def generate_all(self):
        """Generate entire hierarchical wiki"""
        print("\n" + "="*80)
        print("🏗️  GENERATING HIERARCHICAL WIKI")
        print("="*80 + "\n")
        
        for category_id, category_info in self.structure.items():
            category_path = self.output_dir / category_id
            category_path.mkdir(exist_ok=True)
            
            print(f"\n📁 Category: {category_info['title']}")
            print("-" * 80)
            
            # Generate category index if prompt exists
            if "index_prompt" in category_info:
                title, content = await self.generate_section(
                    f"{category_info['title']} - Index",
                    category_info["index_prompt"],
                    mode="mix",
                    top_k=100,
                    breadcrumb=f"Home > {category_info['title']}"
                )
                if content:
                    self._write_file(
                        category_path / "README.md",
                        f"# {category_info['title']}\n\n{content}"
                    )
            
            # Generate pages
            if "pages" in category_info:
                for page in category_info["pages"]:
                    breadcrumb = f"Home > {category_info['title']} > {page['title']}"
                    title, content = await self.generate_section(
                        page["title"],
                        page["prompt"],
                        mode=page["mode"],
                        top_k=page["top_k"],
                        breadcrumb=breadcrumb
                    )
                    if content:
                        filepath = category_path / f"{page['name']}.md"
                        self._write_file(
                            filepath,
                            f"# {page['title']}\n\n{content}"
                        )
                        self.generated_pages.append((category_id, page['name'], page['title']))
            
            # Generate subfolders
            if "subfolders" in category_info:
                await self._generate_subfolders(
                    category_path,
                    category_info["subfolders"],
                    f"Home > {category_info['title']}"
                )
        
        # Generate root index
        await self.generate_root_index()
        
        print("\n" + "="*80)
        print("✅ WIKI GENERATION COMPLETE!")
        print(f"📂 Output: {self.output_dir}")
        print(f"📄 Generated {len(self.generated_pages)} pages")
        print("="*80 + "\n")
    
    async def _generate_subfolders(self, parent_path: Path, subfolders: Dict, breadcrumb: str):
        """Recursively generate subfolders"""
        for folder_name, folder_content in subfolders.items():
            folder_path = parent_path / folder_name
            folder_path.mkdir(exist_ok=True)
            
            print(f"   📂 Subfolder: {folder_name}")
            
            if "pages" in folder_content:
                for page in folder_content["pages"]:
                    page_breadcrumb = f"{breadcrumb} > {folder_name.title()} > {page['title']}"
                    title, content = await self.generate_section(
                        page["title"],
                        page["prompt"],
                        mode=page["mode"],
                        top_k=page["top_k"],
                        breadcrumb=page_breadcrumb
                    )
                    if content:
                        filepath = folder_path / f"{page['name']}.md"
                        self._write_file(
                            filepath,
                            f"# {page['title']}\n\n{content}"
                        )
                        self.generated_pages.append((folder_name, page['name'], page['title']))
    
    async def generate_root_index(self):
        """Generate root README with full hierarchy"""
        content = """# LightRAG Repository Wiki

Welcome to the comprehensive LightRAG documentation!

This wiki was automatically generated from the codebase using LightRAG's knowledge graph.

## 📚 Table of Contents

"""
        for category_id, category_info in self.structure.items():
            content += f"### [{category_info['title']}]({category_id}/README.md)\n\n"
            
            if "pages" in category_info:
                for page in category_info["pages"][:5]:
                    content += f"- [{page['title']}]({category_id}/{page['name']}.md)\n"
            
            if "subfolders" in category_info:
                for subfolder in list(category_info["subfolders"].keys())[:3]:
                    content += f"- [{subfolder.title()}]({category_id}/{subfolder}/)\n"
            
            content += "\n"
        
        content += """
---

## 🚀 Quick Links

- [Getting Started](03-guides/getting-started.md)
- [API Reference](04-api-reference/quick-start.md)
- [FAQ](06-troubleshooting/faq.md)

---

*Generated using LightRAG*
"""
        
        self._write_file(self.output_dir / "README.md", content)
        print("📋 Generated root index")


async def main():
    """Main entry point"""
    
    # Paths
    working_dir = Path(__file__).parent / "lightrag_storage"
    output_dir = Path(__file__).parent / "wiki_docs"
    
    print("=" * 80)
    print("LIGHTRAG WIKI GENERATOR")
    print("=" * 80)
    print(f"\n📁 Storage: {working_dir}")
    print(f"📂 Output: {output_dir}\n")
    
    # Initialize generator
    generator = HierarchicalWikiGenerator(
        working_dir=str(working_dir),
        workspace="main",
        output_dir=str(output_dir)
    )
    
    # Generate wiki
    await generator.generate_all()


if __name__ == "__main__":
    asyncio.run(main())
