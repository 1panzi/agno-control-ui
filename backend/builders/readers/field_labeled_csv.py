from typing import Any

from builders.readers.base import BaseReaderBuilder


class FieldLabeledCsvReaderBuilder(BaseReaderBuilder):
    type = "field_labeled_csv"
    label = "字段标记 CSV"

    try:
        from agno.knowledge.reader.field_labeled_csv_reader import FieldLabeledCSVReader
        agno_class = FieldLabeledCSVReader
    except ImportError:
        agno_class = None

    extra_fields = [
        {
            "name": "chunk_title", "type": "str", "default": None, "required": False,
            "label": "条目标题", "group": "字段标记配置", "span": 12, "order": 1,
            "placeholder": "可选标题前缀",
            "tooltip": "每行文档前缀标题，留空不添加",
        },
        {
            "name": "format_headers", "type": "bool", "default": True, "required": False,
            "label": "格式化表头", "group": "字段标记配置", "span": 12, "order": 2,
            "tooltip": "将下划线替换为空格并转为标题格式",
        },
        {
            "name": "skip_empty_fields", "type": "bool", "default": True, "required": False,
            "label": "跳过空字段", "group": "字段标记配置", "span": 12, "order": 3,
            "tooltip": "跳过值为空的字段",
        },
    ]

    async def build(self, config: dict, resolver) -> Any:
        from agno.knowledge.reader.field_labeled_csv_reader import FieldLabeledCSVReader
        kwargs: dict = {}
        for k in ("chunk_title", "format_headers", "skip_empty_fields"):
            if config.get(k) is not None:
                kwargs[k] = config[k]
        return FieldLabeledCSVReader(**kwargs)
