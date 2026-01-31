"""Prompt templates for wiki generation"""
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class PageDefinition:
    """Definition of a wiki page"""
    name: str
    title: str
    mode: str  # global, local, mix, hybrid, naive
    top_k: int
    prompt: str


def get_wiki_structure() -> Dict:
    """Define the hierarchical wiki structure with prompts"""
    
    return {
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
        # Add more categories here...
    }


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
