"""
JsonDbBuilder — 本地 JSON 文件存储后端。

将数据以 JSON 文件形式存储在本地目录中。
"""

from typing import Any

from builders.dbs.base import DbBuilder, _table_kwargs


class JsonDbBuilder(DbBuilder):
    category = "db"
    type = "json"
    label = "JSON 文件"

    extra_fields = [
        {
            "name": "db_path",
            "type": "str",
            "required": False,
            "order": 1,
            "placeholder": "./agno_json_db（留空使用默认路径）",
        },
        *DbBuilder.extra_fields,
    ]

    field_meta = {
        "db_path": {"label": "存储目录路径", "group": "连接配置", "span": 24,
                    "tooltip": "JSON 文件存储目录，留空使用当前目录下的 agno_json_db"},
        **DbBuilder.field_meta,
    }

    async def build(self, config: dict, resolver) -> Any:
        from agno.db.json.json_db import JsonDb

        kwargs = _table_kwargs(config)
        if config.get("db_path"):
            kwargs["db_path"] = config["db_path"]

        return JsonDb(**kwargs)
