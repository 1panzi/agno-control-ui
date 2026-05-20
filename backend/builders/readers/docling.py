from typing import Any

from builders.readers.base import BaseReaderBuilder


class DoclingReaderBuilder(BaseReaderBuilder):
    type = "docling"
    label = "Docling 多格式文档"

    try:
        from agno.knowledge.reader.docling_reader import DoclingReader
        agno_class = DoclingReader
    except ImportError:
        agno_class = None

    extra_fields = [
        {
            "name": "output_format", "type": "select", "default": "markdown", "required": False,
            "label": "输出格式", "group": "Docling 配置", "span": 12, "order": 1,
            "options": [
                {"value": "markdown", "label": "Markdown"},
                {"value": "text", "label": "纯文本"},
                {"value": "json", "label": "JSON"},
                {"value": "yaml", "label": "YAML"},
                {"value": "html", "label": "HTML"},
                {"value": "html_split_page", "label": "HTML（分页）"},
                {"value": "doctags", "label": "DocTags"},
                {"value": "vtt", "label": "WebVTT"},
            ],
            "tooltip": "Docling 转换后的输出格式",
        },
    ]

    async def build(self, config: dict, resolver) -> Any:
        from agno.knowledge.reader.docling_reader import DoclingReader
        chunker = await self._build_chunker(config, resolver)
        kwargs: dict = {
            "chunk": config.get("chunk", True),
            "chunk_size": config.get("chunk_size", 5000),
        }
        if chunker is not None:
            kwargs["chunking_strategy"] = chunker
        if config.get("output_format"):
            kwargs["output_format"] = config["output_format"]
        return DoclingReader(**kwargs)
