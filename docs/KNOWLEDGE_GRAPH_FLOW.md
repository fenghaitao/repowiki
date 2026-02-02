# Knowledge Graph Flow: Visual Guide

## Complete Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    STEP 1: INDEXING                             │
│                  (Build Knowledge Graph)                         │
└─────────────────────────────────────────────────────────────────┘

Repository Files                    LightRAG Processing
─────────────────                   ──────────────────
┌──────────────┐
│  config.py   │ ──┐
│  main.py     │   │
│  utils.py    │   ├──> Read & Chunk ──> Extract Entities
│  README.md   │   │                      ┌─────────────┐
└──────────────┘ ──┘                      │ Config      │
                                          │ main()      │
                                          │ Utils       │
                                          │ Path        │
                                          └─────────────┘
                                                 │
                                                 ↓
                                          Extract Relationships
                                          ┌──────────────────┐
                                          │ main uses Config │
                                          │ Config uses Path │
                                          │ Utils provides X │
                                          └──────────────────┘
                                                 │
                                                 ↓
                                          Create Embeddings
                                          (Semantic vectors)
                                                 │
                                                 ↓
                                          Build Knowledge Graph
                                          ┌──────────────────┐
                                          │   [main()]       │
                                          │      ↓ uses      │
                                          │   [Config]       │
                                          │      ↓ uses      │
                                          │    [Path]        │
                                          │                  │
                                          │   [Utils]        │
                                          │      ↓ provides  │
                                          │   [helpers]      │
                                          └──────────────────┘
                                                 │
                                                 ↓
                                          Store in Files
                                          ┌──────────────────┐
                                          │ graph.graphml    │
                                          │ entities.json    │
                                          │ relations.json   │
                                          │ embeddings.json  │
                                          └──────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    STEP 2: GENERATION                           │
│                 (Query Knowledge Graph)                          │
└─────────────────────────────────────────────────────────────────┘

Wiki Structure                      Query Process
──────────────                      ─────────────
┌──────────────┐
│ 01-overview  │ ──┐
│ 02-getting   │   │
│ 03-concepts  │   ├──> For each page:
│ 04-api       │   │    ┌────────────────────────────────┐
│ 05-dev       │   │    │ 1. Get prompt from prompts.py  │
└──────────────┘ ──┘    │    "Describe architecture..."  │
                        │                                │
                        │ 2. Query knowledge graph       │
                        │    mode = "global"             │
                        │    top_k = 30                  │
                        │                                │
                        │ 3. LightRAG searches graph     │
                        │    ┌─────────────────────┐    │
                        │    │ Find: Config,       │    │
                        │    │       Indexer,      │    │
                        │    │       Generator     │    │
                        │    │                     │    │
                        │    │ Relationships:      │    │
                        │    │   CLI -> Indexer   │    │
                        │    │   CLI -> Generator │    │
                        │    └─────────────────────┘    │
                        │                                │
                        │ 4. Retrieve context            │
                        │    (top 30 relevant chunks)    │
                        │                                │
                        │ 5. Send to LLM                 │
                        │    Prompt + Context            │
                        │                                │
                        │ 6. LLM generates doc           │
                        │    "The system follows..."     │
                        │                                │
                        │ 7. Write to file               │
                        │    architecture.md             │
                        └────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                  PARALLEL EXECUTION                             │
└─────────────────────────────────────────────────────────────────┘

Category: 01-overview
├── Task 1: project-overview.md  ──┐
├── Task 2: architecture.md        ├──> asyncio.gather()
└── Task 3: design-decisions.md  ──┘         │
                                              ↓
                                    ┌──────────────────┐
                                    │ Query Graph (1)  │
                                    │ Query Graph (2)  │ ← Parallel!
                                    │ Query Graph (3)  │
                                    └──────────────────┘
                                              │
                                              ↓
                                    ┌──────────────────┐
                                    │ LLM Call (1)     │
                                    │ LLM Call (2)     │ ← 96 concurrent
                                    │ LLM Call (3)     │
                                    └──────────────────┘
                                              │
                                              ↓
                                    ┌──────────────────┐
                                    │ Write File (1)   │
                                    │ Write File (2)   │
                                    │ Write File (3)   │
                                    └──────────────────┘

Result: 3 pages in ~2 seconds instead of ~6 seconds!
```

## Query Mode Comparison

```
┌─────────────────────────────────────────────────────────────────┐
│                      GLOBAL MODE                                │
│              "What's the big picture?"                          │
└─────────────────────────────────────────────────────────────────┘

Prompt: "Describe the overall architecture"

Knowledge Graph:                    Search Strategy:
                                   ─────────────────
    [CLI]                          1. Start from high-level nodes
      ↓                            2. Follow major relationships
   [Indexer] [Generator]           3. Aggregate patterns
      ↓           ↓                4. Return: broad overview
   [LightRAG]  [LightRAG]
      ↓           ↓
   [Storage]  [Prompts]            Result:
                                   "System has 3 main components:
                                    CLI, Indexer, Generator.
                                    They work together in a pipeline..."

┌─────────────────────────────────────────────────────────────────┐
│                      LOCAL MODE                                 │
│            "Tell me about this specific thing"                  │
└─────────────────────────────────────────────────────────────────┘

Prompt: "Document the Config class API"

Knowledge Graph:                    Search Strategy:
                                   ─────────────────
    [Config]                       1. Find specific entity (Config)
      ↓                            2. Get immediate neighbors
   [repo_path]                     3. Look at direct relationships
   [working_dir]                   4. Return: detailed info
   [validate()]
   [from_env()]                    Result:
                                   "Config class:
                                    - repo_path: Path to repository
                                    - validate(): Validates config
                                    - from_env(): Creates from env vars
                                    Methods: ..."

┌─────────────────────────────────────────────────────────────────┐
│                      HYBRID MODE                                │
│              "Give me both overview and details"                │
└─────────────────────────────────────────────────────────────────┘

Prompt: "How do I configure the system?"

Knowledge Graph:                    Search Strategy:
                                   ─────────────────
    [Config]                       1. Combine global + local
      ↓                            2. Find config-related everywhere
   [ENV_VARS]                      3. Get patterns + specifics
      ↓                            4. Return: comprehensive guide
   [CLI_ARGS]
      ↓                            Result:
   [Examples]                      "Configuration options:
                                    1. Environment variables
                                    2. Config class
                                    3. CLI arguments
                                    Examples: [from multiple files]"
```

## Real Example: Generating "Architecture" Page

```
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: Get Page Definition                                    │
└─────────────────────────────────────────────────────────────────┘

From prompts.py:
────────────────
PageDefinition(
    name="architecture",
    title="Architecture",
    mode="global",      ← Use global mode for high-level view
    top_k=30,          ← Get 30 most relevant pieces
    prompt="""
    Analyze the codebase architecture and describe:
    1. Overall Architecture Pattern
    2. Core Components
    3. Data Flow
    """
)

┌─────────────────────────────────────────────────────────────────┐
│ Step 2: Query Knowledge Graph                                  │
└─────────────────────────────────────────────────────────────────┘

await rag.aquery(
    prompt="Analyze the codebase architecture...",
    param=QueryParam(mode="global", top_k=30)
)

LightRAG Internal Process:
──────────────────────────
1. Parse prompt → keywords: ["architecture", "components", "data flow"]

2. Search graph for relevant entities:
   ┌─────────────────────────────────────┐
   │ Found entities (scored by relevance):│
   │ - Config (0.95)                     │
   │ - Indexer (0.92)                    │
   │ - Generator (0.91)                  │
   │ - WikiGenerator (0.89)              │
   │ - LightRAG (0.87)                   │
   │ - CLI (0.85)                        │
   │ ... (24 more)                       │
   └─────────────────────────────────────┘

3. Get relationships between top entities:
   ┌─────────────────────────────────────┐
   │ CLI uses Indexer                    │
   │ CLI uses Generator                  │
   │ Indexer uses LightRAG               │
   │ Generator uses LightRAG             │
   │ Generator uses Config               │
   │ Indexer uses Config                 │
   └─────────────────────────────────────┘

4. Retrieve code chunks (top 30):
   ┌─────────────────────────────────────┐
   │ Chunk 1: Config class definition    │
   │ Chunk 2: Indexer class definition   │
   │ Chunk 3: Generator class definition │
   │ Chunk 4: CLI main function          │
   │ Chunk 5: LightRAG initialization    │
   │ ... (25 more chunks)                │
   └─────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Step 3: Send to LLM                                            │
└─────────────────────────────────────────────────────────────────┘

LLM receives:
─────────────
System: You are a technical documentation expert.

Context from knowledge graph:
────────────────────────────
[30 code chunks with entities and relationships]

Example chunks:
- "Config class manages configuration with repo_path, working_dir..."
- "Indexer builds knowledge graph by reading files and calling rag.ainsert..."
- "Generator queries graph with rag.aquery to create documentation..."
- "CLI orchestrates: run_index() then run_generate()..."

User prompt:
───────────
Analyze the codebase architecture and describe:
1. Overall Architecture Pattern
2. Core Components  
3. Data Flow

┌─────────────────────────────────────────────────────────────────┐
│ Step 4: LLM Generates Documentation                            │
└─────────────────────────────────────────────────────────────────┘

LLM Output:
──────────
# Architecture

## Overall Architecture Pattern

The system follows a **pipeline architecture** with three main stages:

1. **Indexing**: Reads repository files and builds knowledge graph
2. **Storage**: Maintains graph in LightRAG format
3. **Generation**: Queries graph to create documentation

## Core Components

### 1. Config
- Manages configuration (paths, models, settings)
- Auto-detects repository name from git
- Validates settings before use

### 2. Indexer
- Collects files from repository
- Reads and chunks content
- Inserts into LightRAG knowledge graph

### 3. Generator
- Queries knowledge graph with strategic prompts
- Uses different modes (global/local/hybrid)
- Generates hierarchical wiki structure

### 4. CLI
- Orchestrates the workflow
- Provides commands: index, generate, all, test

## Data Flow

1. User runs `repowiki index`
2. CLI creates Indexer with Config
3. Indexer collects files → reads content → inserts to LightRAG
4. LightRAG builds graph (entities + relationships + embeddings)
5. User runs `repowiki generate`
6. CLI creates Generator with Config
7. Generator queries LightRAG with prompts
8. LightRAG returns relevant context from graph
9. Generator sends context to LLM
10. LLM generates documentation
11. Generator writes to wiki_docs/

┌─────────────────────────────────────────────────────────────────┐
│ Step 5: Write to File                                          │
└─────────────────────────────────────────────────────────────────┘

write_file(
    path="wiki_docs/01-overview/architecture.md",
    content=llm_output
)

Result: ✅ Generated: Architecture
```

## Performance: Parallel vs Sequential

```
Sequential (Old Way):
─────────────────────
Page 1: Query → LLM → Write (2s)
Page 2: Query → LLM → Write (2s)
Page 3: Query → LLM → Write (2s)
Total: 6 seconds

Parallel (Current Way):
───────────────────────
Page 1: Query ──┐
Page 2: Query ──┼──> LLM (all at once) ──> Write all
Page 3: Query ──┘
Total: 2 seconds

With 13 pages:
Sequential: 26 seconds
Parallel: 2-3 seconds (10x faster!)
```

## Summary

**Knowledge Graph = Smart Database**
- Stores code structure, not just text
- Understands relationships
- Enables semantic search

**Query Modes = Different Lenses**
- Global: Wide angle (architecture, overview)
- Local: Zoom in (specific APIs, details)
- Hybrid: Both (configuration, guides)

**Parallel Processing = Speed**
- Multiple queries simultaneously
- 96 concurrent LLM calls
- Result: 28 seconds for 19 pages

**The Magic:**
1. Build graph once (10 hours)
2. Query many times (seconds)
3. High-quality docs automatically
