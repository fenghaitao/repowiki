"""Prompt templates for wiki generation

Refined prompts based on reference implementation with:
- More focused, single-purpose prompts
- Strategic mode selection (global/local/hybrid)
- Better top_k values (30-40 range)
- Practical sections (dependencies, testing, extension_points)
"""
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
                    top_k=30,
                    prompt="""
Based on the codebase knowledge graph, provide a comprehensive overview of this project.

Include:
- What the project does (main purpose)
- Key features and capabilities
- Primary use cases
- Target audience (who would use this)
- High-level architecture approach

Be concise but comprehensive (2-3 paragraphs). Focus on what makes this project unique.
"""
                ),
                PageDefinition(
                    name="architecture",
                    title="Architecture",
                    mode="global",
                    top_k=30,
                    prompt="""
Analyze the codebase architecture and describe:

1. Overall Architecture Pattern
   - What architectural pattern is used? (MVC, microservices, layered, etc.)
   - Why was this pattern chosen?

2. Core Components
   - What are the main modules/packages?
   - How do they interact?

3. Data Flow
   - How does data flow through the system?
   - What are the main entry points?

Provide a clear, structured explanation suitable for developers.
"""
                ),
                PageDefinition(
                    name="design-decisions",
                    title="Design Decisions",
                    mode="global",
                    top_k=30,
                    prompt="""
Explain the core concepts and design principles of this codebase.

Identify:
- Key abstractions and what they represent
- Important design patterns used (if any)
- Domain-specific terminology
- Mental models developers should understand

This should help developers understand the "philosophy" of the codebase.
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
                    title="Getting Started",
                    mode="hybrid",
                    top_k=35,
                    prompt="""
Create a "Getting Started" guide based on the codebase.

Include:
1. Installation
   - Prerequisites (languages, tools, versions)
   - Installation steps
   - Environment setup

2. Basic Usage
   - Simplest way to use the project
   - First example
   - Expected output

3. Configuration
   - Required configuration
   - Common settings

Be practical and actionable for someone new to the project.
"""
                ),
                PageDefinition(
                    name="configuration",
                    title="Configuration Guide",
                    mode="hybrid",
                    top_k=35,
                    prompt="""
Document configuration options:

1. Main Configuration
   - Configuration file format
   - Key settings and their purpose
   - Default values

2. Environment Variables
   - Available environment variables
   - How they override config

3. Advanced Configuration
   - Performance tuning options
   - Custom settings

Format as reference guide with examples.
"""
                ),
            ]
        },
        
        "03-core-concepts": {
            "title": "Core Concepts",
            "pages": [
                PageDefinition(
                    name="key-components",
                    title="Key Components",
                    mode="local",
                    top_k=40,
                    prompt="""
Identify and describe the 5-10 most important components/modules in this codebase.

For each key component, provide:
- Component name
- Primary responsibility (one sentence)
- Key classes/functions within it
- What it depends on

Organize by importance and functionality.
"""
                ),
                PageDefinition(
                    name="project-structure",
                    title="Project Structure",
                    mode="hybrid",
                    top_k=35,
                    prompt="""
Explain the directory/package structure of this codebase.

For the main directories:
- Directory name
- Purpose
- What types of files belong there

This helps developers navigate the codebase.
"""
                ),
                PageDefinition(
                    name="common-workflows",
                    title="Common Workflows",
                    mode="global",
                    top_k=30,
                    prompt="""
Describe 2-3 common workflows or processes in this codebase.

For each workflow:
- Workflow name
- Step-by-step process
- Components involved

Focus on workflows that represent core functionality.
"""
                ),
            ]
        },
        
        "04-api-reference": {
            "title": "API Reference",
            "pages": [
                PageDefinition(
                    name="public-api",
                    title="Public API",
                    mode="local",
                    top_k=40,
                    prompt="""
Extract and document the main public APIs of this codebase.

For each major API/interface:
- API name and purpose
- Main methods/functions
- Parameters and return types
- Brief usage example

Focus on APIs that external users would interact with.
Organize by functionality (e.g., Authentication API, Data API, etc.)
"""
                ),
                PageDefinition(
                    name="code-examples",
                    title="Code Examples",
                    mode="local",
                    top_k=40,
                    prompt="""
Provide 3-5 practical code examples showing how to use this codebase.

For each example:
- Clear title explaining the use case
- Actual code snippet
- Brief explanation of what it does

Focus on common, real-world scenarios.
"""
                ),
            ]
        },
        
        "05-development": {
            "title": "Development Guide",
            "pages": [
                PageDefinition(
                    name="dependencies",
                    title="Dependencies",
                    mode="hybrid",
                    top_k=35,
                    prompt="""
Analyze the dependencies of this codebase.

List:
1. External Dependencies
   - Major libraries/packages used
   - Purpose of each major dependency

2. System Requirements
   - Platform requirements (OS, runtime)
   - Minimum versions if critical

Be concise but cover the most important dependencies.
"""
                ),
                PageDefinition(
                    name="testing",
                    title="Testing Guide",
                    mode="hybrid",
                    top_k=35,
                    prompt="""
Describe the testing approach in this codebase.

Cover:
- Types of tests (unit, integration, e2e)
- Testing frameworks used
- How to run tests
- How to write new tests

Be practical and actionable.
"""
                ),
                PageDefinition(
                    name="extension-points",
                    title="Extension Points",
                    mode="hybrid",
                    top_k=35,
                    prompt="""
Describe how this codebase can be extended or customized.

Include:
- Plugin/extension mechanisms (if any)
- Customization points
- How to add new features
- Best practices for extending

This helps developers who want to build on the codebase.
"""
                ),
            ]
        },
    }
    
    return {**base_structure, **extended_structure}


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
