from typing import Any

from builders.readers.base import BaseReaderBuilder


class ExcelReaderBuilder(BaseReaderBuilder):
    type = "excel"
    label = "Excel 表格"

    try:
        from agno.knowledge.reader.excel_reader import ExcelReader
        agno_class = ExcelReader
    except ImportError:
        agno_class = None

    extra_fields = [
        {
            "name": "sheets", "type": "str", "default": None, "required": False,
            "label": "工作表过滤", "group": "Excel 配置", "span": 24, "order": 1,
            "placeholder": "Sheet1, Sheet2, 1, 2",
            "tooltip": "要读取的工作表名称或编号（逗号分隔），留空读取全部",
        },
    ]

    async def build(self, config: dict, resolver) -> Any:
        from agno.knowledge.reader.excel_reader import ExcelReader
        chunker = await self._build_chunker(config, resolver)
        kwargs: dict = {
            "chunk": config.get("chunk", True),
            "chunk_size": config.get("chunk_size", 5000),
        }
        if chunker is not None:
            kwargs["chunking_strategy"] = chunker
        if config.get("sheets"):
            raw = config["sheets"]
            sheets = []
            for s in raw.split(","):
                s = s.strip()
                if s.isdigit():
                    sheets.append(int(s))
                elif s:
                    sheets.append(s)
            if sheets:
                kwargs["sheets"] = sheets
        return ExcelReader(**kwargs)
