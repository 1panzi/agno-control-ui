"""
GcsJsonDbBuilder — Google Cloud Storage JSON 文件存储后端。

将数据以 JSON 文件形式存储在 GCS 存储桶中。
"""

from typing import Any

from builders.dbs.base import DbBuilder, _table_kwargs


class GcsJsonDbBuilder(DbBuilder):
    category = "db"
    type = "gcs_json"
    label = "GCS JSON"

    extra_fields = [
        {
            "name": "bucket_name",
            "type": "str",
            "required": True,
            "order": 1,
            "placeholder": "my-agno-bucket",
        },
        {
            "name": "prefix",
            "type": "str",
            "required": False,
            "order": 2,
            "placeholder": "agno/（留空使用默认前缀）",
        },
        {
            "name": "project",
            "type": "str",
            "required": False,
            "order": 3,
            "placeholder": "GCP 项目 ID（留空使用默认）",
        },
        *DbBuilder.extra_fields,
    ]

    field_meta = {
        "bucket_name": {"label": "存储桶名称", "group": "连接配置", "span": 24},
        "prefix":      {"label": "路径前缀", "group": "连接配置", "span": 12,
                        "tooltip": "GCS 中文件的路径前缀，默认 agno/"},
        "project":     {"label": "GCP 项目 ID", "group": "连接配置", "span": 12},
        **DbBuilder.field_meta,
    }

    async def build(self, config: dict, resolver) -> Any:
        from agno.db.gcs_json.gcs_json_db import GcsJsonDb

        kwargs = _table_kwargs(config)
        kwargs["bucket_name"] = config["bucket_name"]
        if config.get("prefix"):
            kwargs["prefix"] = config["prefix"]
        if config.get("project"):
            kwargs["project"] = config["project"]

        return GcsJsonDb(**kwargs)
