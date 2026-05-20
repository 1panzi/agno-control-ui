from typing import Any

from builders.readers.base import BaseReaderBuilder


class PptxReaderBuilder(BaseReaderBuilder):
    type = "pptx"
    label = "PowerPoint 演示文稿"

    try:
        from agno.knowledge.reader.pptx_reader import PPTXReader
        agno_class = PPTXReader
    except ImportError:
        agno_class = None

    async def build(self, config: dict, resolver) -> Any:
        from agno.knowledge.reader.pptx_reader import PPTXReader
        chunker = await self._build_chunker(config, resolver)
        kwargs: dict = {
            "chunk": config.get("chunk", True),
            "chunk_size": config.get("chunk_size", 5000),
        }
        if chunker is not None:
            kwargs["chunking_strategy"] = chunker
        return PPTXReader(**kwargs)
