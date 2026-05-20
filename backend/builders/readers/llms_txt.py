from typing import Any

from builders.readers.base import BaseReaderBuilder


class LlmsTxtReaderBuilder(BaseReaderBuilder):
    type = "llms_txt"
    label = "LLMs.txt"

    try:
        from agno.knowledge.reader.llms_txt_reader import LLMsTxtReader
        agno_class = LLMsTxtReader
    except ImportError:
        agno_class = None

    extra_fields = [
        {
            "name": "max_urls", "type": "int", "default": 20, "required": False,
            "label": "最大 URL 数", "group": "LLMs.txt 配置", "span": 8, "order": 1,
            "min": 1, "max": 200,
            "tooltip": "从 llms.txt 中抓取的最大链接数",
        },
        {
            "name": "timeout", "type": "int", "default": 60, "required": False,
            "label": "超时（秒）", "group": "LLMs.txt 配置", "span": 8, "order": 2,
            "min": 1, "max": 300,
        },
        {
            "name": "proxy", "type": "str", "default": None, "required": False,
            "label": "代理", "group": "LLMs.txt 配置", "span": 8, "order": 3,
            "placeholder": "http://proxy:port",
        },
        {
            "name": "skip_optional", "type": "bool", "default": False, "required": False,
            "label": "跳过 Optional 章节", "group": "LLMs.txt 配置", "span": 12, "order": 4,
        },
    ]

    async def build(self, config: dict, resolver) -> Any:
        from agno.knowledge.reader.llms_txt_reader import LLMsTxtReader
        chunker = await self._build_chunker(config, resolver)
        kwargs: dict = {
            "chunk": config.get("chunk", True),
            "chunk_size": config.get("chunk_size", 5000),
        }
        if chunker is not None:
            kwargs["chunking_strategy"] = chunker
        for k in ("max_urls", "timeout", "proxy", "skip_optional"):
            if config.get(k) is not None:
                kwargs[k] = config[k]
        return LLMsTxtReader(**kwargs)
