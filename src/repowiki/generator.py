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
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.config.validate()
        
        # Add LightRAG to path
        sys.path.insert(0, str(self.config.lightrag_repo))
        
        # Set API key in environment (for LightRAG)
        os.environ["OPENAI_API_KEY"] = self.config.api_key
        
        # Import LightRAG
        from lightrag import LightRAG, QueryParam
        from lightrag.llm import openai_complete_if_cache, openai_embedding
        
        self.LightRAG = LightRAG
        self.QueryParam = QueryParam
        self.llm_func = openai_complete_if_cache
        self.embedding_func = openai_embedding
        
        print(f"🤖 Using GitHub Copilot models (like lightrag_openspec)")
        print(f"   LLM: {self.config.llm_model_name}")
        
        self.rag = None
        self.generated_pages = []
    
    def initialize_rag(self):
        """Initialize LightRAG instance"""
        self.rag = self.LightRAG(
            working_dir=str(self.config.working_dir),
            workspace=self.config.workspace,
            llm_model_func=self.llm_func,
            embedding_func=self.embedding_func,
            llm_model_name=self.config.llm_model_name,
            embedding_model_name=self.config.embedding_model_name,
        )
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
        
        # Generate pages
        if "pages" in category_info:
            for page in category_info["pages"]:
                breadcrumb = f"Home > {category_info['title']} > {page.title}"
                title, content = await self.generate_page(
                    page.title,
                    page.prompt,
                    mode=page.mode,
                    top_k=page.top_k,
                    breadcrumb=breadcrumb
                )
                if content:
                    filepath = category_path / f"{page.name}.md"
                    self.write_file(
                        filepath,
                        f"# {page.title}\n\n{content}"
                    )
                    self.generated_pages.append((category_id, page.name, page.title))
    
    async def generate_root_index(self, structure: Dict):
        """Generate root README with full hierarchy"""
        content = """# LightRAG Repository Wiki

Welcome to the comprehensive LightRAG documentation!

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
        print("🏗️  GENERATING HIERARCHICAL WIKI")
        print("="*80 + "\n")
        
        # Initialize RAG
        self.initialize_rag()
        
        # Get wiki structure
        structure = get_wiki_structure()
        
        # Generate each category
        for category_id, category_info in structure.items():
            await self.generate_category(category_id, category_info)
        
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
