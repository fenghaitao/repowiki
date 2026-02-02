# Knowledge Graph Search: The Complete Prompt Flow

## Overview

When you query the knowledge graph, LightRAG uses **TWO separate prompts**:

1. **Keyword Extraction Prompt** - Extracts search keywords from your query
2. **RAG Response Prompt** - Generates the final answer using retrieved context

## Step-by-Step Process

```
Your Query: "Describe the overall architecture"
        ↓
┌───────────────────────────────────────────────────────────────┐
│ STEP 1: Extract Keywords (Search the Graph)                  │
└───────────────────────────────────────────────────────────────┘

LLM Call #1: Keyword Extraction
────────────────────────────────

Prompt sent to LLM:
───────────────────
---Role---
You are an expert keyword extractor, specializing in analyzing 
user queries for a Retrieval-Augmented Generation (RAG) system.

---Goal---
Extract two distinct types of keywords:
1. high_level_keywords: overarching concepts or themes
2. low_level_keywords: specific entities or details

---Examples---
Example 1:
Query: "How does international trade influence global economic stability?"
Output:
{
  "high_level_keywords": ["International trade", "Global economic stability"],
  "low_level_keywords": ["Trade agreements", "Tariffs", "Currency exchange"]
}

Example 2:
Query: "What are the environmental consequences of deforestation?"
Output:
{
  "high_level_keywords": ["Environmental consequences", "Deforestation"],
  "low_level_keywords": ["Species extinction", "Habitat destruction"]
}

---Real Data---
User Query: Describe the overall architecture

---Output---
Output:

LLM Response:
─────────────
{
  "high_level_keywords": ["architecture", "system design", "overall structure"],
  "low_level_keywords": ["components", "modules", "classes", "functions"]
}

        ↓
┌───────────────────────────────────────────────────────────────┐
│ STEP 2: Search Knowledge Graph with Keywords                 │
└───────────────────────────────────────────────────────────────┘

Using extracted keywords:
─────────────────────────

High-level keywords: ["architecture", "system design", "overall structure"]
Low-level keywords: ["components", "modules", "classes", "functions"]

Search Strategy (mode="global"):
────────────────────────────────
1. Search entities_vdb with high-level keywords
   → Find: Config, Indexer, Generator, WikiGenerator, LightRAG

2. Search relationships_vdb with high-level keywords
   → Find: "CLI uses Indexer", "Generator uses LightRAG"

3. Get top_k=30 most relevant results

4. Retrieve associated code chunks from text_chunks_db

Result: Context with 30 relevant chunks
────────────────────────────────────────

        ↓
┌───────────────────────────────────────────────────────────────┐
│ STEP 3: Generate Answer with Context                         │
└───────────────────────────────────────────────────────────────┘

LLM Call #2: Generate Answer
─────────────────────────────

Prompt sent to LLM:
───────────────────
---Role---
You are an expert AI assistant specializing in synthesizing 
information from a provided knowledge base.

---Goal---
Generate a comprehensive, well-structured answer to the user query.

---Instructions---
1. Scrutinize both Knowledge Graph Data and Document Chunks
2. Extract all pieces of information that are directly relevant
3. Weave the extracted facts into a coherent response
4. Base your answer STRICTLY on the provided Context

---Context---

## Knowledge Graph Data

### Entities:
1. Config (type: class)
   - Description: Manages configuration with repo_path, working_dir
   - Relationships: used_by [Indexer, Generator]

2. Indexer (type: class)
   - Description: Indexes repository into knowledge graph
   - Relationships: uses [Config, LightRAG]

3. Generator (type: class)
   - Description: Generates wiki from knowledge graph
   - Relationships: uses [Config, LightRAG]

### Relationships:
- CLI uses Indexer
- CLI uses Generator
- Indexer uses LightRAG
- Generator uses LightRAG

## Document Chunks

[1] File: src/repowiki/config.py
```python
@dataclass
class Config:
    """Repowiki configuration"""
    repo_path: Path = Path(".")
    ...
```

[2] File: src/repowiki/indexer.py
```python
class RepositoryIndexer:
    """Indexes a code repository"""
    ...
```

... (28 more chunks)

---Response Type---
Multiple Paragraphs

---User Query---
Describe the overall architecture

LLM Response:
─────────────
The system follows a pipeline architecture with three main stages:

1. **Indexing**: The RepositoryIndexer reads files from the repository
   and builds a knowledge graph using LightRAG...

2. **Storage**: The knowledge graph is maintained in LightRAG format
   with entities, relationships, and embeddings...

3. **Generation**: The WikiGenerator queries the knowledge graph
   to create hierarchical documentation...

[Full detailed response]
```

## The Two Prompts in Detail

### Prompt 1: Keyword Extraction

**Purpose**: Convert natural language query into searchable keywords

**Location**: `lightrag/prompt.py` - `PROMPTS["keywords_extraction"]`

**Template**:
```python
"""---Role---
You are an expert keyword extractor, specializing in analyzing 
user queries for a Retrieval-Augmented Generation (RAG) system.

---Goal---
Extract two distinct types of keywords:
1. high_level_keywords: for overarching concepts or themes
2. low_level_keywords: for specific entities or details

---Instructions & Constraints---
1. Output Format: Valid JSON object only
2. Source of Truth: All keywords from user query
3. Concise & Meaningful: Multi-word phrases when appropriate
4. Handle Edge Cases: Empty lists for vague queries
5. Language: All keywords in {language}

---Examples---
{examples}

---Real Data---
User Query: {query}

---Output---
Output:"""
```

**Example Input/Output**:
```
Input: "Describe the overall architecture"

Output:
{
  "high_level_keywords": ["architecture", "system design", "overall structure"],
  "low_level_keywords": ["components", "modules", "classes", "functions"]
}
```

### Prompt 2: RAG Response

**Purpose**: Generate answer using retrieved context

**Location**: `lightrag/prompt.py` - `PROMPTS["rag_response"]`

**Template**:
```python
"""---Role---
You are an expert AI assistant specializing in synthesizing 
information from a provided knowledge base.

---Goal---
Generate a comprehensive, well-structured answer to the user query.
The answer must integrate relevant facts from the Knowledge Graph 
and Document Chunks found in the Context.

---Instructions---
1. Step-by-Step Instruction:
  - Determine the user's query intent
  - Scrutinize both Knowledge Graph Data and Document Chunks
  - Extract all relevant information
  - Weave facts into coherent response
  - Track reference_id for citations
  - Generate references section

2. Content & Grounding:
  - Base answer STRICTLY on provided Context
  - Do NOT use external knowledge
  - If Context lacks info, state this clearly

---Context---
{context_data}

---Response Type---
{response_type}

---User Query---
{user_prompt}
"""
```

## Query Modes and Keyword Usage

### Global Mode
```python
mode = "global"
top_k = 30

# Uses: high_level_keywords only
# Searches: relationships_vdb
# Purpose: Find broad patterns and high-level structure
# Example keywords: ["architecture", "system design"]
```

### Local Mode
```python
mode = "local"
top_k = 40

# Uses: low_level_keywords only
# Searches: entities_vdb
# Purpose: Find specific entities and details
# Example keywords: ["Config", "Indexer", "generate_page"]
```

### Hybrid Mode
```python
mode = "hybrid"
top_k = 35

# Uses: BOTH high_level and low_level keywords
# Searches: entities_vdb AND relationships_vdb
# Purpose: Combine broad patterns with specific details
# Example keywords: ["architecture", "Config", "Indexer"]
```

## Code Location

### Keyword Extraction
```python
# File: lightrag/operate.py
# Function: extract_keywords_only()
# Line: ~3260

async def extract_keywords_only(text, param, global_config, hashing_kv):
    # Build keyword extraction prompt
    kw_prompt = PROMPTS["keywords_extraction"].format(
        query=text,
        examples=examples,
        language=language,
    )
    
    # Call LLM to extract keywords
    result = await use_model_func(kw_prompt, keyword_extraction=True)
    
    # Parse JSON response
    keywords_data = json_repair.loads(result)
    return (
        keywords_data.get("high_level_keywords", []),
        keywords_data.get("low_level_keywords", [])
    )
```

### Knowledge Graph Search
```python
# File: lightrag/operate.py
# Function: _build_query_context()
# Line: ~2800

async def _build_query_context(
    query, ll_keywords_str, hl_keywords_str, ...
):
    # Search entities with low-level keywords
    if mode in ["local", "hybrid", "mix"]:
        entities = await entities_vdb.query(ll_keywords_str, top_k=top_k)
    
    # Search relationships with high-level keywords
    if mode in ["global", "hybrid", "mix"]:
        relationships = await relationships_vdb.query(hl_keywords_str, top_k=top_k)
    
    # Get associated document chunks
    chunks = await get_chunks_for_entities(entities, relationships)
    
    # Format as context string
    context = format_context(entities, relationships, chunks)
    
    return context
```

### Answer Generation
```python
# File: lightrag/operate.py
# Function: kg_query()
# Line: ~3120

async def kg_query(query, ...):
    # 1. Extract keywords
    hl_keywords, ll_keywords = await get_keywords_from_query(query)
    
    # 2. Build context from knowledge graph
    context_result = await _build_query_context(
        query, ll_keywords_str, hl_keywords_str, ...
    )
    
    # 3. Build RAG response prompt with context
    sys_prompt = PROMPTS["rag_response"].format(
        context_data=context_result.context,
        response_type=response_type,
        user_prompt=user_prompt,
    )
    
    # 4. Call LLM to generate answer
    response = await use_model_func(query, system_prompt=sys_prompt)
    
    return response
```

## Real Example: "Describe the architecture"

### Step 1: Keyword Extraction

**Input**: "Describe the overall architecture"

**LLM Call**:
```
Prompt: [keywords_extraction template with query]
Response: {
  "high_level_keywords": ["architecture", "system design", "structure"],
  "low_level_keywords": ["components", "modules", "Config", "Indexer"]
}
```

### Step 2: Knowledge Graph Search

**Search with keywords**:
```python
# Global mode uses high-level keywords
relationships = await relationships_vdb.query(
    "architecture, system design, structure",
    top_k=30
)

# Results:
# - CLI uses Indexer (relevance: 0.92)
# - CLI uses Generator (relevance: 0.91)
# - Indexer uses LightRAG (relevance: 0.89)
# - Generator uses LightRAG (relevance: 0.88)
# ... (26 more)
```

### Step 3: Build Context

**Format results**:
```
## Knowledge Graph Data

### Entities:
1. Config (class) - Manages configuration
2. Indexer (class) - Indexes repository
3. Generator (class) - Generates wiki

### Relationships:
- CLI uses Indexer
- CLI uses Generator
- Indexer uses LightRAG

## Document Chunks
[1] src/repowiki/config.py: class Config...
[2] src/repowiki/indexer.py: class RepositoryIndexer...
...
```

### Step 4: Generate Answer

**LLM Call**:
```
System Prompt: [rag_response template with context]
User Query: "Describe the overall architecture"
Response: [Detailed architecture description]
```

## Summary

**Two-Stage Process**:

1. **Keyword Extraction** (LLM Call #1)
   - Input: Your natural language query
   - Prompt: `keywords_extraction`
   - Output: JSON with high/low-level keywords
   - Purpose: Convert query to searchable terms

2. **Answer Generation** (LLM Call #2)
   - Input: Your query + Retrieved context
   - Prompt: `rag_response`
   - Output: Final answer
   - Purpose: Generate answer from context

**Why Two Prompts?**
- Separation of concerns: Search vs. Answer
- Better search: Keywords are more precise than full query
- Caching: Keywords can be cached separately
- Flexibility: Different modes use different keyword types

**The Magic**:
- You ask: "Describe the architecture"
- LightRAG extracts: ["architecture", "system design", "components"]
- LightRAG searches: Knowledge graph with keywords
- LightRAG retrieves: 30 relevant chunks
- LightRAG generates: Comprehensive answer from chunks
- You get: Detailed architecture documentation
