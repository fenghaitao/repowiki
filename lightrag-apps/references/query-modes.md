# LightRAG Query Modes

LightRAG supports multiple query modes for retrieving information from the knowledge graph.

## Available Modes

### Global Mode
- **Use case**: High-level overview questions
- **Behavior**: Searches across the entire codebase
- **Example**: "What is the overall architecture?"

### Local Mode
- **Use case**: Specific implementation details
- **Behavior**: Focuses on local context and specific components
- **Example**: "How does the Config class work?"

### Mix Mode
- **Use case**: Questions requiring both overview and details
- **Behavior**: Combines global and local search results
- **Example**: "How do the indexer and generator interact?"

### Hybrid Mode
- **Use case**: Balanced queries (default)
- **Behavior**: Intelligently balances breadth and depth
- **Example**: "Explain the workflow from indexing to generation"

### Naive Mode
- **Use case**: Simple keyword search
- **Behavior**: Basic text matching without graph traversal
- **Example**: "Find all references to 'async'"

## Mode Selection Guidelines

| Question Type | Recommended Mode |
|--------------|------------------|
| Project overview | Global |
| API documentation | Local |
| Architecture | Hybrid |
| Workflows | Mix |
| Specific class/function | Local |
| Design decisions | Global |
| Integration points | Hybrid |
| Code examples | Local |

## Performance Characteristics

- **Global**: Slower, comprehensive results
- **Local**: Faster, focused results
- **Mix**: Moderate speed, balanced results
- **Hybrid**: Adaptive, generally optimal
- **Naive**: Fastest, basic matching

## Usage in Wiki Generation

The wiki generator automatically selects appropriate modes for different sections:

- **Overview sections**: Global mode
- **API reference**: Local mode
- **Architecture docs**: Hybrid mode
- **Examples**: Mix mode
