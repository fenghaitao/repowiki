# Complete Prompt Flow: From prompts.py to LLM

## YES! The prompts in prompts.py are the user queries!

Here's the complete flow showing how your prompts become the queries:

## The Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. PROMPTS.PY - Your Wiki Generation Prompts                   │
└─────────────────────────────────────────────────────────────────┘

File: src/repowiki/prompts.py
──────────────────────────────

PageDefinition(
    name="architecture",
    title="Architecture",
    mode="global",
    top_k=30,
    prompt="""
Analyze the codebase architecture and describe:

1. Overall Architecture Pattern
   - What architectural pattern is used?
   - Why was this pattern chosen?

2. Core Components
   - What are the main modules/packages?
   - How do they interact?

3. Data Flow
   - How does data flow through the system?
   - What are the main entry points?

Provide a clear, structured explanation suitable for developers.
"""
)

        ↓

┌─────────────────────────────────────────────────────────────────┐
│ 2. GENERATOR.PY - Sends Prompt to Knowledge Graph              │
└─────────────────────────────────────────────────────────────────┘

File: src/repowiki/generator.py
────────────────────────────────

async def generate_page(self, title, prompt, mode, top_k):
    """Generate a single wiki page"""
    
    # This prompt is from prompts.py!
    result = await self.rag.aquery(
        prompt,                    # ← Your prompt from prompts.py
        param=QueryParam(
            mode=mode,             # ← "global" from prompts.py
            top_k=top_k            # ← 30 from prompts.py
        )
    )
    
    return result

        ↓

┌─────────────────────────────────────────────────────────────────┐
│ 3. LIGHTRAG - Extracts Keywords from Your Prompt               │
└─────────────────────────────────────────────────────────────────┘

File: lightrag/operate.py
─────────────────────────

async def kg_query(query, ...):
    # query = your prompt from prompts.py
    
    # Extract keywords from YOUR prompt
    hl_keywords, ll_keywords = await get_keywords_from_query(query)

LLM Call #1: Keyword Extraction
────────────────────────────────

System Prompt: [keywords_extraction template]

User Query: """
Analyze the codebase architecture and describe:
1. Overall Architecture Pattern
2. Core Components
3. Data Flow
"""
                    ↑
                    └── This is YOUR prompt from prompts.py!

LLM Response:
{
  "high_level_keywords": ["architecture", "pattern", "components", "data flow"],
  "low_level_keywords": ["modules", "packages", "entry points", "system"]
}

        ↓

┌─────────────────────────────────────────────────────────────────┐
│ 4. LIGHTRAG - Searches Knowledge Graph with Keywords           │
└─────────────────────────────────────────────────────────────────┘

Vector Search (No LLM)
──────────────────────

# Search with extracted keywords
entities = await entities_vdb.query("architecture, pattern, components", top_k=30)
relationships = await relationships_vdb.query("architecture, pattern", top_k=30)

# Retrieve context
context = build_context(entities, relationships, chunks)

        ↓

┌─────────────────────────────────────────────────────────────────┐
│ 5. LIGHTRAG - Generates Answer with Context                    │
└─────────────────────────────────────────────────────────────────┘

LLM Call #2: Generate Answer
─────────────────────────────

System Prompt: """
---Role---
You are an expert AI assistant...

---Context---
[Retrieved from knowledge graph:
 - Config class
 - Indexer class
 - Generator class
 - Relationships between them
 - Code chunks
]

---Response Type---
Multiple Paragraphs

---User Query---
n/a
"""

User Query: """
Analyze the codebase architecture and describe:
1. Overall Architecture Pattern
2. Core Components
3. Data Flow
"""
    ↑
    └── Still YOUR prompt from prompts.py!

LLM Response:
"""
The system follows a pipeline architecture with three main stages:

1. **Overall Architecture Pattern**
   The codebase uses a pipeline architecture where data flows through
   distinct stages: indexing, storage, and generation...

2. **Core Components**
   - Config: Manages configuration
   - Indexer: Builds knowledge graph
   - Generator: Creates wiki documentation
   ...

3. **Data Flow**
   Files → Indexer → LightRAG → Storage → Generator → Wiki
   ...
"""

        ↓

┌─────────────────────────────────────────────────────────────────┐
│ 6. GENERATOR.PY - Writes to File                               │
└─────────────────────────────────────────────────────────────────┘

File: src/repowiki/generator.py
────────────────────────────────

write_file(
    path="wiki_docs/01-overview/architecture.md",
    content=llm_response
)

Result: ✅ Generated: Architecture
```

## The Key Insight

**Your prompts from `prompts.py` are used in TWO places:**

1. **As input to keyword extraction** (LLM Call #1)
   - LightRAG extracts keywords FROM your prompt
   - These keywords search the knowledge graph

2. **As the user query** (LLM Call #2)
   - Your prompt is sent to the LLM again
   - But this time WITH context from the knowledge graph
   - LLM answers YOUR prompt using the retrieved context

## Real Example

### Your Prompt (prompts.py)
```python
prompt="""
Analyze the codebase architecture and describe:

1. Overall Architecture Pattern
2. Core Components
3. Data Flow
"""
```

### What Happens

**Step 1: Extract Keywords**
```
Input: Your prompt
Output: ["architecture", "pattern", "components", "data flow"]
```

**Step 2: Search Knowledge Graph**
```
Search with: ["architecture", "pattern", "components"]
Found: Config, Indexer, Generator, relationships, code chunks
```

**Step 3: Generate Answer**
```
System: Here's what I found in the codebase [context]
User: Analyze the codebase architecture and describe... [your prompt]
LLM: The system follows a pipeline architecture... [answer]
```

## Code Locations

### 1. Your Prompts
```python
# File: src/repowiki/prompts.py
# Line: ~40-70

PageDefinition(
    name="architecture",
    prompt="""Analyze the codebase architecture..."""  # ← Your prompt
)
```

### 2. Sending to LightRAG
```python
# File: src/repowiki/generator.py
# Line: ~105

result = await self.rag.aquery(
    page.prompt,  # ← Your prompt from prompts.py
    param=QueryParam(mode=page.mode, top_k=page.top_k)
)
```

### 3. Keyword Extraction
```python
# File: lightrag/operate.py
# Line: ~3070

hl_keywords, ll_keywords = await get_keywords_from_query(
    query  # ← Your prompt from prompts.py
)
```

### 4. Final Answer Generation
```python
# File: lightrag/operate.py
# Line: ~3140

response = await use_model_func(
    query,  # ← Your prompt from prompts.py (again!)
    system_prompt=sys_prompt  # ← With context embedded
)
```

## Summary

**YES!** The prompts in `prompts.py` are the user queries that:

1. ✅ Get sent to LLM for keyword extraction
2. ✅ Keywords search the knowledge graph
3. ✅ Get sent to LLM again with retrieved context
4. ✅ LLM generates answer based on YOUR prompt + context

**Your prompt is used twice:**
- First: To extract search keywords
- Second: As the actual question to answer (with context)

**This is why good prompts matter!**
- Clear prompts → Better keywords → Better search → Better context → Better answers
- Your prompts in `prompts.py` directly control what information is retrieved and how it's presented

## Example: Different Prompts, Different Results

### Prompt 1: Vague
```python
prompt="Tell me about the code"
```
**Result**: Vague keywords → Poor search → Generic answer

### Prompt 2: Specific (What we use)
```python
prompt="""
Analyze the codebase architecture and describe:
1. Overall Architecture Pattern
2. Core Components
3. Data Flow
"""
```
**Result**: Specific keywords → Targeted search → Detailed answer

### Prompt 3: Too Narrow
```python
prompt="What is the Config class?"
```
**Result**: Only Config-related keywords → Misses broader context

**Our prompts are carefully crafted to:**
- Be specific enough to get relevant results
- Be broad enough to capture context
- Guide the LLM to structure the answer properly
- Use the right query mode (global/local/hybrid)
