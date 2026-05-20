from typing import Any

from builders.readers.base import BaseReaderBuilder


class WebSearchReaderBuilder(BaseReaderBuilder):
    type = "web_search"
    label = "网页搜索"

    try:
        from agno.knowledge.reader.web_search_reader import WebSearchReader
        agno_class = WebSearchReader
    except ImportError:
        agno_class = None

    extra_fields = [
        {
            "name": "search_timeout", "type": "int", "default": 10, "required": False,
            "label": "搜索超时（秒）", "group": "搜索配置", "span": 8, "order": 1,
            "min": 1, "max": 120,
        },
        {
            "name": "request_timeout", "type": "int", "default": 30, "required": False,
            "label": "请求超时（秒）", "group": "搜索配置", "span": 8, "order": 2,
            "min": 1, "max": 300,
        },
        {
            "name": "delay_between_requests", "type": "float", "default": 2.0, "required": False,
            "label": "请求间隔（秒）", "group": "搜索配置", "span": 8, "order": 3,
            "min": 0.0, "max": 30.0, "step": 0.5,
        },
        {
            "name": "max_retries", "type": "int", "default": 3, "required": False,
            "label": "最大重试次数", "group": "搜索配置", "span": 8, "order": 4,
            "min": 0, "max": 10,
        },
    ]

    async def build(self, config: dict, resolver) -> Any:
        from agno.knowledge.reader.web_search_reader import WebSearchReader
        chunker = await self._build_chunker(config, resolver)
        kwargs: dict = {
            "chunk": config.get("chunk", True),
            "chunk_size": config.get("chunk_size", 5000),
        }
        if chunker is not None:
            kwargs["chunking_strategy"] = chunker
        for k in ("search_timeout", "request_timeout", "delay_between_requests", "max_retries"):
            if config.get(k) is not None:
                kwargs[k] = config[k]
        return WebSearchReader(**kwargs)
