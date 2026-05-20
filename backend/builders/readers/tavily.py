from typing import Any

from builders.readers.base import BaseReaderBuilder


class TavilyReaderBuilder(BaseReaderBuilder):
    type = "tavily"
    label = "Tavily 网页提取"

    try:
        from agno.knowledge.reader.tavily_reader import TavilyReader
        agno_class = TavilyReader
    except ImportError:
        agno_class = None

    extra_fields = [
        {
            "name": "api_key", "type": "password", "default": None, "required": False,
            "label": "API Key", "group": "Tavily 配置", "span": 24, "order": 1,
            "tooltip": "Tavily API 密钥（或设置 TAVILY_API_KEY 环境变量）",
        },
        {
            "name": "extract_format", "type": "select", "default": "markdown", "required": False,
            "label": "提取格式", "group": "Tavily 配置", "span": 12, "order": 2,
            "options": [
                {"value": "markdown", "label": "Markdown"},
                {"value": "text", "label": "纯文本"},
            ],
        },
        {
            "name": "extract_depth", "type": "select", "default": "basic", "required": False,
            "label": "提取深度", "group": "Tavily 配置", "span": 12, "order": 3,
            "options": [
                {"value": "basic", "label": "基础"},
                {"value": "advanced", "label": "高级"},
            ],
            "tooltip": "basic: 1 credit/5 URLs, advanced: 2 credits/5 URLs",
        },
    ]

    async def build(self, config: dict, resolver) -> Any:
        from agno.knowledge.reader.tavily_reader import TavilyReader
        chunker = await self._build_chunker(config, resolver)
        kwargs: dict = {
            "chunk": config.get("chunk", True),
            "chunk_size": config.get("chunk_size", 5000),
        }
        if chunker is not None:
            kwargs["chunking_strategy"] = chunker
        for k in ("api_key", "extract_format", "extract_depth"):
            if config.get(k) is not None:
                kwargs[k] = config[k]
        return TavilyReader(**kwargs)
