"""
MongoDbBuilder — MongoDB 存储后端。

通过 db_url 或 db_name 连接，使用 collection 名替代 table 名。
"""

from typing import Any

from builders.dbs.base import DbBuilder


class MongoDbBuilder(DbBuilder):
    category = "db"
    type = "mongo"
    label = "MongoDB"

    extra_fields = [
        {
            "name": "db_url",
            "type": "str",
            "required": False,
            "order": 1,
            "placeholder": "mongodb://localhost:27017",
        },
        {
            "name": "db_name",
            "type": "str",
            "required": False,
            "order": 2,
            "placeholder": "agno",
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
        "db_url":               {"label": "数据库 URL", "group": "连接配置", "span": 24},
        "db_name":              {"label": "数据库名", "group": "连接配置", "span": 24},
        "session_collection":   {"label": "会话集合名", "group": "集合配置（高级）", "span": 12, "placeholder": "留空使用默认"},
        "memory_collection":    {"label": "记忆集合名", "group": "集合配置（高级）", "span": 12, "placeholder": "留空使用默认"},
        "metrics_collection":   {"label": "指标集合名", "group": "集合配置（高级）", "span": 12, "placeholder": "留空使用默认"},
        "knowledge_collection": {"label": "知识库集合名", "group": "集合配置（高级）", "span": 12, "placeholder": "留空使用默认"},
        "culture_collection":   {"label": "文化集合名", "group": "集合配置（高级）", "span": 12, "placeholder": "留空使用默认"},
        "traces_collection":    {"label": "追踪集合名", "group": "集合配置（高级）", "span": 12, "placeholder": "留空使用默认"},
        "spans_collection":     {"label": "Span集合名", "group": "集合配置（高级）", "span": 12, "placeholder": "留空使用默认"},
    }

    async def build(self, config: dict, resolver) -> Any:
        from agno.db.mongo.mongo import MongoDb

        kwargs: dict = {}
        if config.get("db_url"):
            kwargs["db_url"] = config["db_url"]
        if config.get("db_name"):
            kwargs["db_name"] = config["db_name"]
        for key in [
            "session_collection", "memory_collection", "metrics_collection",
            "knowledge_collection", "culture_collection", "traces_collection",
            "spans_collection",
        ]:
            if config.get(key):
                kwargs[key] = config[key]

        return MongoDb(**kwargs)
