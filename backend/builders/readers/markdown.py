from typing import Any

from builders.readers.base import BaseReaderBuilder


class MarkdownReaderBuilder(BaseReaderBuilder):
    type = "markdown"
    label = "Markdown 文档"

    try:
        from agno.knowledge.reader.markdown_reader import MarkdownReader
        agno_class = MarkdownReader
    except ImportError:
        agno_class = None

    async def build(self, config: dict, resolver) -> Any:
        from agno.knowledge.reader.markdown_reader import MarkdownReader
        chunker = await self._build_chunker(config, resolver)
        kwargs: dict = {
            "chunk": config.get("chunk", True),
            "chunk_size": config.get("chunk_size", 5000),
        }
        if chunker is not None:
            kwargs["chunking_strategy"] = chunker
        return MarkdownReader(**kwargs)
