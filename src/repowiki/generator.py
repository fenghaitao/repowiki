"""Wiki generator - creates hierarchical documentation from knowledge graph"""
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import asyncio

from .config import Config
from .prompts import get_wiki_structure, get_category_index_prompt


class WikiGenerator:
    """Generates hierarchical wiki documentation from knowledge graph"""
    
    def __init__(self, config: Optional[Config] = None, extended: bool = False):
        self.config = config or Config()
        self.config.validate()
        self.extended = extended
        
        # Set API key in environment
        os.environ["OPENAI_API_KEY"] = self.config.api_key
        
        # Import LightRAG (assumes it's installed via pip)
        from lightrag import LightRAG, QueryParam
        from lightrag.llm.llama_index_impl import (
            llama_index_complete_if_cache,
            llama_index_embed,
        )
        from lightrag.utils import EmbeddingFunc
        from llama_index.llms.litellm import LiteLLM
        from llama_index.embeddings.litellm import LiteLLMEmbedding
        
        self.EmbeddingFunc = EmbeddingFunc
        self.LightRAG = LightRAG
        self.QueryParam = QueryParam
        self.llama_index_complete_if_cache = llama_index_complete_if_cache
        self.llama_index_embed = llama_index_embed
        self.LiteLLM = LiteLLM
        self.LiteLLMEmbedding = LiteLLMEmbedding
        
        print(f"🤖 Using GitHub Copilot models")
        print(f"   LLM: {self.config.llm_model_name}")
        
        self.rag = None
        self.generated_pages = []
    
    async def _create_llm_func(self, prompt, system_prompt=None, history_messages=[], **kwargs):
        """Create LLM function using LiteLLM."""
        if "llm_instance" not in kwargs:
            kwargs["llm_instance"] = self.LiteLLM(
                model=self.config.llm_model_name,
                api_key=self.config.api_key,
                temperature=0.7,
            )
        return await self.llama_index_complete_if_cache(
            kwargs["llm_instance"], prompt, system_prompt, history_messages
        )
    
    async def _create_embedding_func(self, texts):
        """Create embedding function using LiteLLM."""
        embed_model = self.LiteLLMEmbedding(
            model_name=self.config.embedding_model_name,
            api_key=self.config.api_key,
        )
        return await self.llama_index_embed(texts, embed_model=embed_model)
    
    async def initialize_rag(self):
        """Initialize LightRAG instance"""
        # Wrap embedding function with EmbeddingFunc
        embedding_func_wrapped = self.EmbeddingFunc(
            embedding_dim=1536,  # text-embedding-3-small dimension
            max_token_size=8192,
            func=self._create_embedding_func,
        )
        
        self.rag = self.LightRAG(
            working_dir=str(self.config.working_dir),
            workspace=self.config.workspace,
            llm_model_func=self._create_llm_func,
            embedding_func=embedding_func_wrapped,
            llm_model_name=self.config.llm_model_name,
            # Parallel processing configuration (same as indexer for consistency)
            llm_model_max_async=self.config.llm_model_max_async,
            embedding_func_max_async=self.config.embedding_func_max_async,
        )
        # Initialize storages
        await self.rag.initialize_storages()
        return self.rag
    
    async def generate_page(
        self,
        title: str,
        prompt: str,
        mode: str = "global",
        top_k: int = 60,
        breadcrumb: str = ""
    ) -> Tuple[str, Optional[str]]:
        """Generate a single wiki page"""
        print(f"📝 Generating: {title}...")
        
        try:
            # Add breadcrumb to prompt
            enhanced_prompt = f"BREADCRUMB: {breadcrumb}\n\n{prompt}\n\nInclude breadcrumb at the top."
            
            result = await self.rag.aquery(
                enhanced_prompt,
                param=self.QueryParam(
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
    
    def write_file(self, path: Path, content: str):
        """Write content to file"""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    async def generate_category(
        self,
        category_id: str,
        category_info: Dict
    ):
        """Generate all pages in a category"""
        category_path = self.config.output_dir / category_id
        category_path.mkdir(exist_ok=True)
        
        print(f"\n📁 Category: {category_info['title']}")
        print("-" * 80)
        
        # Generate category index if needed
        if "index_prompt" in category_info or "pages" in category_info:
            index_prompt = category_info.get(
                "index_prompt",
                get_category_index_prompt(category_info["title"])
            )
            title, content = await self.generate_page(
                f"{category_info['title']} - Index",
                index_prompt,
                mode="mix",
                top_k=100,
                breadcrumb=f"Home > {category_info['title']}"
            )
            if content:
                self.write_file(
                    category_path / "README.md",
                    f"# {category_info['title']}\n\n{content}"
                )
        
        # Generate pages in parallel
        if "pages" in category_info:
            # Create all page generation tasks
            page_tasks = []
            for page in category_info["pages"]:
                breadcrumb = f"Home > {category_info['title']} > {page.title}"
                task = self.generate_page(
                    page.title,
                    page.prompt,
                    mode=page.mode,
                    top_k=page.top_k,
                    breadcrumb=breadcrumb
                )
                page_tasks.append((page, task))
            
            # Execute all pages in parallel
            results = await asyncio.gather(*[task for _, task in page_tasks])
            
            # Write results
            for (page, _), (title, content) in zip(page_tasks, results):
                if content:
                    filepath = category_path / f"{page.name}.md"
                    self.write_file(
                        filepath,
                        f"# {page.title}\n\n{content}"
                    )
                    self.generated_pages.append((category_id, page.name, page.title))
    
    async def generate_root_index(self, structure: Dict):
        """Generate root README with full hierarchy"""
        content = f"""# {self.config.repo_name} Repository Wiki

Welcome to the comprehensive {self.config.repo_name} documentation!

This wiki was automatically generated from the codebase using LightRAG's knowledge graph.

## 📚 Table of Contents

"""
        for category_id, category_info in structure.items():
            content += f"### [{category_info['title']}]({category_id}/README.md)\n\n"
            
            if "pages" in category_info:
                for page in category_info["pages"][:5]:
                    content += f"- [{page.title}]({category_id}/{page.name}.md)\n"
            
            content += "\n"
        
        content += """
---

## 🚀 Quick Links

- [Getting Started](03-guides/getting-started.md)
- [API Reference](04-api-reference/quick-start.md)
- [FAQ](06-troubleshooting/faq.md)

---

*Generated using LightRAG with GitHub Copilot models*
"""
        
        self.write_file(self.config.output_dir / "README.md", content)
        print("📋 Generated root index")
    
    async def generate_all(self):
        """Generate entire hierarchical wiki"""
        print("\n" + "="*80)
        print("🏗️  GENERATING HIERARCHICAL WIKI (PARALLEL MODE)")
        print("="*80 + "\n")
        
        # Initialize RAG
        await self.initialize_rag()
        
        # Get wiki structure
        structure = get_wiki_structure(extended=self.extended)
        
        # Generate all categories in parallel
        category_tasks = [
            self.generate_category(category_id, category_info)
            for category_id, category_info in structure.items()
        ]
        await asyncio.gather(*category_tasks)
        
        # Generate root index
        await self.generate_root_index(structure)
        
        print("\n" + "="*80)
        print("✅ WIKI GENERATION COMPLETE!")
        print(f"📂 Output: {self.config.output_dir}")
        print(f"📄 Generated {len(self.generated_pages)} pages")
        print("="*80 + "\n")


async def main():
    """CLI entry point for generator"""
    config = Config.from_env()
    generator = WikiGenerator(config)
    await generator.generate_all()


if __name__ == "__main__":
    asyncio.run(main())
