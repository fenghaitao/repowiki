"""Prompt templates for wiki generation"""
from typing import Dict
from dataclasses import dataclass


@dataclass
class PageDefinition:
    """Definition of a wiki page"""
    name: str
    title: str
    mode: str  # global, local, mix, hybrid, naive
    top_k: int
    prompt: str


def get_wiki_structure(extended: bool = False) -> Dict:
    """Define the hierarchical wiki structure with prompts
    
    Args:
        extended: If True, include extended categories for comprehensive documentation
    """
    
    base_structure = {
        "01-overview": {
            "title": "Overview & Architecture",
            "pages": [
                PageDefinition(
                    name="project-overview",
                    title="Project Overview",
                    mode="global",
                    top_k=100,
                    prompt="""
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
                ),
                PageDefinition(
                    name="architecture",
                    title="Architecture",
                    mode="global",
                    top_k=100,
                    prompt="""
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

Format as markdown that can be used to generate a diagram.
"""
                ),
                PageDefinition(
                    name="design-decisions",
                    title="Design Decisions",
                    mode="global",
                    top_k=100,
                    prompt="""
Identify key design decisions in LightRAG:

1. **Architectural Choices**
   - Why flat entity-relation graph instead of hierarchical communities?
   - Trade-offs made (speed vs sophistication)

2. **Technology Choices**
   - Why these specific frameworks/libraries?
   - Why support 12+ storage backends?

3. **Developer Experience**
   - Why simple API?
   - Why incremental updates?
   - Why multi-workspace support?

Present as "Design Decisions" document explaining rationale.
"""
                ),
            ]
        },
    }
    
    if not extended:
        return base_structure
    
    # Extended structure for comprehensive documentation
    extended_structure = {
        "02-getting-started": {
            "title": "Getting Started",
            "pages": [
                PageDefinition(
                    name="installation",
                    title="Installation Guide",
                    mode="mix",
                    top_k=80,
                    prompt="""
Create a comprehensive installation guide:

1. **System Requirements**
   - Python version
   - Operating systems supported
   - Dependencies

2. **Installation Methods**
   - pip install
   - Docker installation
   - From source
   - Kubernetes deployment

3. **Configuration**
   - Environment variables
   - Config files
   - API keys setup

4. **Verification**
   - How to test installation
   - First steps

Format with code examples and troubleshooting tips.
"""
                ),
                PageDefinition(
                    name="quick-start",
                    title="Quick Start Tutorial",
                    mode="mix",
                    top_k=100,
                    prompt="""
Create a quick start tutorial:

1. **First Example**
   - Simplest working code
   - What each line does

2. **Basic Operations**
   - Insert documents
   - Query the knowledge graph
   - View results

3. **Common Patterns**
   - Typical usage scenarios
   - Best practices

Include complete, runnable code examples.
"""
                ),
                PageDefinition(
                    name="configuration",
                    title="Configuration Guide",
                    mode="hybrid",
                    top_k=120,
                    prompt="""
Document all configuration options:

1. **LLM Configuration**
   - Model selection
   - API keys
   - Model parameters

2. **Storage Configuration**
   - Graph storage backends
   - Vector storage backends
   - KV storage backends

3. **Performance Tuning**
   - Parallel processing settings
   - Cache configuration
   - Timeout settings

4. **Advanced Options**
   - Custom prompts
   - Chunking strategies

Format as reference guide with examples.
"""
                ),
            ]
        },
        
        "03-api-reference": {
            "title": "API Reference",
            "pages": [
                PageDefinition(
                    name="lightrag-api",
                    title="LightRAG Core API",
                    mode="hybrid",
                    top_k=150,
                    prompt="""
Document the LightRAG class API:

1. **Class: LightRAG**
   - Constructor parameters
   - All public methods
   - Return types

2. **Main Methods**
   - insert() / ainsert()
   - query() / aquery()
   - delete()
   - update()

3. **Query Modes**
   - naive, local, global, hybrid, mix
   - When to use each mode
   - Parameters for each

4. **Examples**
   - Code snippets for each method

Format as API documentation with signatures.
"""
                ),
                PageDefinition(
                    name="storage-api",
                    title="Storage Backend API",
                    mode="hybrid",
                    top_k=120,
                    prompt="""
Document storage backend interfaces:

1. **GraphStorage Interface**
   - Required methods
   - Implementation examples

2. **VectorStorage Interface**
   - Required methods
   - Embedding handling

3. **KVStorage Interface**
   - Required methods
   - JSON vs database backends

4. **Custom Storage Backends**
   - How to implement your own
   - Registration process

Include code examples and interface definitions.
"""
                ),
                PageDefinition(
                    name="rest-api",
                    title="REST API Reference",
                    mode="mix",
                    top_k=100,
                    prompt="""
Document the REST API server:

1. **Server Setup**
   - How to start the API server
   - Configuration

2. **Endpoints**
   - Document management endpoints
   - Query endpoints
   - Graph visualization endpoints

3. **Request/Response Formats**
   - JSON schemas
   - Authentication

4. **Examples**
   - curl commands
   - Python requests examples

Format as REST API documentation.
"""
                ),
            ]
        },
        
        "04-storage-backends": {
            "title": "Storage Backends",
            "pages": [
                PageDefinition(
                    name="graph-storage",
                    title="Graph Storage Options",
                    mode="hybrid",
                    top_k=120,
                    prompt="""
Document all graph storage backends:

1. **Available Backends**
   - NetworkX (default)
   - Neo4j
   - Memgraph
   - PostgreSQL

2. **Comparison**
   - Features of each
   - Performance characteristics
   - When to use which

3. **Setup & Configuration**
   - Installation requirements
   - Configuration examples
   - Connection strings

4. **Migration**
   - Switching between backends
   - Data export/import

Include pros/cons and code examples.
"""
                ),
                PageDefinition(
                    name="vector-storage",
                    title="Vector Storage Options",
                    mode="hybrid",
                    top_k=120,
                    prompt="""
Document all vector storage backends:

1. **Available Backends**
   - Nano Vector DB (default)
   - Milvus
   - Qdrant
   - FAISS
   - Redis

2. **Comparison**
   - Scalability
   - Performance
   - Feature matrix

3. **Setup & Configuration**
   - Installation
   - Configuration examples
   - Index creation

4. **Best Practices**
   - Choosing embedding dimensions
   - Index tuning

Include setup examples and benchmarks.
"""
                ),
                PageDefinition(
                    name="kv-storage",
                    title="Key-Value Storage Options",
                    mode="mix",
                    top_k=100,
                    prompt="""
Document all KV storage backends:

1. **Available Backends**
   - JSON files (default)
   - MongoDB
   - Redis
   - PostgreSQL

2. **Use Cases**
   - When to use each
   - Trade-offs

3. **Configuration**
   - Setup examples
   - Connection parameters

4. **Performance**
   - Benchmarks
   - Optimization tips

Format with comparison table.
"""
                ),
            ]
        },
        
        "05-llm-integration": {
            "title": "LLM Integration",
            "pages": [
                PageDefinition(
                    name="supported-llms",
                    title="Supported LLM Providers",
                    mode="hybrid",
                    top_k=150,
                    prompt="""
Document all supported LLM providers:

1. **List of Providers**
   - OpenAI
   - Azure OpenAI
   - Ollama
   - Google Gemini
   - Anthropic Claude
   - Hugging Face
   - vLLM
   - LMDeploy
   - Others

2. **For Each Provider**
   - Setup instructions
   - Configuration
   - Example code
   - Supported models

3. **Model Selection**
   - Recommended models
   - Performance vs cost

Include complete setup examples.
"""
                ),
                PageDefinition(
                    name="custom-llm",
                    title="Custom LLM Integration",
                    mode="mix",
                    top_k=80,
                    prompt="""
How to integrate custom LLM providers:

1. **LLM Function Interface**
   - Required signature
   - Parameters
   - Return format

2. **Embedding Function Interface**
   - Required signature
   - Vector dimensions

3. **Implementation Example**
   - Complete working example
   - Error handling
   - Caching integration

4. **Testing**
   - How to test your integration

Format as tutorial with code.
"""
                ),
            ]
        },
        
        "06-examples": {
            "title": "Examples & Tutorials",
            "pages": [
                PageDefinition(
                    name="basic-examples",
                    title="Basic Usage Examples",
                    mode="mix",
                    top_k=100,
                    prompt="""
Provide basic usage examples:

1. **Simple RAG Pipeline**
   - Index documents
   - Query
   - Display results

2. **Different Query Modes**
   - Example for each mode
   - When to use each

3. **Multi-Document Indexing**
   - Batch processing
   - Progress tracking

4. **Custom Configuration**
   - Changing models
   - Adjusting parameters

All with complete, runnable code.
"""
                ),
                PageDefinition(
                    name="advanced-examples",
                    title="Advanced Usage Patterns",
                    mode="hybrid",
                    top_k=120,
                    prompt="""
Advanced usage examples:

1. **Custom Processors**
   - Document preprocessing
   - Custom chunking

2. **Production Deployment**
   - Docker setup
   - Kubernetes
   - Monitoring

3. **Performance Optimization**
   - Parallel processing
   - Caching strategies

4. **Integration Examples**
   - With web frameworks
   - With databases
   - With existing systems

Include complete examples.
"""
                ),
            ]
        },
    }
    
    return {**base_structure, **extended_structure}


def get_module_index_prompt() -> str:
    """Get prompt for module index generation"""
    return """
Create a comprehensive Module Index for LightRAG:

1. **Module Overview**
   High-level description of how modules are organized

2. **Module Hierarchy**
   Show parent-child relationships in tree format

3. **Module Quick Reference**
   Table with: Module, Purpose, Dependencies, Complexity

4. **Navigation**
   Links to each module's detailed documentation

Format as module map with ASCII tree.
"""


def get_category_index_prompt(category_title: str) -> str:
    """Get prompt for category index"""
    return f"""
Create an index page for the "{category_title}" section:

1. **Section Overview**: What this section covers
2. **Table of Contents**: All pages with 1-line descriptions
3. **Quick Links**: Most important pages
4. **Learning Path**: Recommended reading order

Format as markdown.
"""
