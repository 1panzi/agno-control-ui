"""
FirestoreDbBuilder — Google Cloud Firestore 存储后端。

通过 project_id 连接 Firestore，使用 collection 名替代 table 名。
"""

from typing import Any

from builders.dbs.base import DbBuilder, _table_kwargs


class FirestoreDbBuilder(DbBuilder):
    category = "db"
    type = "firestore"
    label = "Firestore"

    extra_fields = [
        {
            "name": "project_id",
            "type": "str",
            "required": True,
            "order": 1,
            "placeholder": "my-gcp-project",
        },
        {
            "name": "session_collection",
            "type": "str",
            "required": False,
            "order": 10,
        },
        {
            "name": "memory_collection",
            "type": "str",
            "required": False,
            "order": 11,
        },
        {
            "name": "metrics_collection",
            "type": "str",
            "required": False,
            "order": 12,
        },
        {
            "name": "knowledge_collection",
            "type": "str",
            "required": False,
            "order": 13,
        },
        {
            "name": "culture_collection",
            "type": "str",
            "required": False,
            "order": 14,
        },
        {
            "name": "traces_collection",
            "type": "str",
            "required": False,
            "order": 15,
        },
        {
            "name": "spans_collection",
            "type": "str",
            "required": False,
            "order": 16,
        },
    ]

    field_meta = {
        "project_id":           {"label": "GCP 项目 ID", "group": "连接配置", "span": 24},
        "session_collection":   {"label": "会话集合名", "group": "集合配置（高级）", "span": 12, "placeholder": "留空使用默认"},
        "memory_collection":    {"label": "记忆集合名", "group": "集合配置（高级）", "span": 12, "placeholder": "留空使用默认"},
        "metrics_collection":   {"label": "指标集合名", "group": "集合配置（高级）", "span": 12, "placeholder": "留空使用默认"},
        "knowledge_collection": {"label": "知识库集合名", "group": "集合配置（高级）", "span": 12, "placeholder": "留空使用默认"},
        "culture_collection":   {"label": "文化集合名", "group": "集合配置（高级）", "span": 12, "placeholder": "留空使用默认"},
        "traces_collection":    {"label": "追踪集合名", "group": "集合配置（高级）", "span": 12, "placeholder": "留空使用默认"},
        "spans_collection":     {"label": "Span集合名", "group": "集合配置（高级）", "span": 12, "placeholder": "留空使用默认"},
    }

    async def build(self, config: dict, resolver) -> Any:
        from agno.db.firestore.firestore import FirestoreDb

        kwargs: dict = {}
        if config.get("project_id"):
            kwargs["project_id"] = config["project_id"]
        for key in [
            "session_collection", "memory_collection", "metrics_collection",
            "knowledge_collection", "culture_collection", "traces_collection",
            "spans_collection",
        ]:
            if config.get(key):
                kwargs[key] = config[key]

        return FirestoreDb(**kwargs)
