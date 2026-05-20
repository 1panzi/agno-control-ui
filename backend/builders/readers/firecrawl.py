from typing import Any

from builders.readers.base import BaseReaderBuilder


class FirecrawlReaderBuilder(BaseReaderBuilder):
    type = "firecrawl"
    label = "Firecrawl 网页抓取"

    try:
        from agno.knowledge.reader.firecrawl_reader import FirecrawlReader
        agno_class = FirecrawlReader
    except ImportError:
        agno_class = None

    extra_fields = [
        {
            "name": "api_key", "type": "password", "default": None, "required": False,
            "label": "API Key", "group": "Firecrawl 配置", "span": 24, "order": 1,
            "tooltip": "Firecrawl API 密钥",
        },
        {
            "name": "mode", "type": "select", "default": "scrape", "required": False,
            "label": "模式", "group": "Firecrawl 配置", "span": 12, "order": 2,
            "options": [
                {"value": "scrape", "label": "单页抓取"},
                {"value": "crawl", "label": "多页爬取"},
            ],
        },
    ]

    async def build(self, config: dict, resolver) -> Any:
        from agno.knowledge.reader.firecrawl_reader import FirecrawlReader
        chunker = await self._build_chunker(config, resolver)
        kwargs: dict = {
            "chunk": config.get("chunk", True),
            "chunk_size": config.get("chunk_size", 5000),
        }
        if chunker is not None:
            kwargs["chunking_strategy"] = chunker
        for k in ("api_key", "mode"):
            if config.get(k) is not None:
                kwargs[k] = config[k]
        return FirecrawlReader(**kwargs)
