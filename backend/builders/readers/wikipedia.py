from typing import Any

from builders.readers.base import BaseReaderBuilder


class WikipediaReaderBuilder(BaseReaderBuilder):
    type = "wikipedia"
    label = "Wikipedia"

    try:
        from agno.knowledge.reader.wikipedia_reader import WikipediaReader
        agno_class = WikipediaReader
    except ImportError:
        agno_class = None

    extra_fields = [
        {
            "name": "auto_suggest", "type": "bool", "default": True, "required": False,
            "label": "自动建议", "group": "Wikipedia 配置", "span": 12, "order": 1,
            "tooltip": "搜索时启用 Wikipedia 自动建议",
        },
    ]

    async def build(self, config: dict, resolver) -> Any:
        from agno.knowledge.reader.wikipedia_reader import WikipediaReader
        chunker = await self._build_chunker(config, resolver)
        kwargs: dict = {
            "chunk": config.get("chunk", True),
            "chunk_size": config.get("chunk_size", 5000),
        }
        if chunker is not None:
            kwargs["chunking_strategy"] = chunker
        if config.get("auto_suggest") is not None:
            kwargs["auto_suggest"] = config["auto_suggest"]
        return WikipediaReader(**kwargs)
