"""
SurrealDbBuilder — SurrealDB 存储后端。

需要提供 db_url、凭证、命名空间和数据库名。
"""

from typing import Any

from builders.dbs.base import DbBuilder, _table_kwargs


class SurrealDbBuilder(DbBuilder):
    category = "db"
    type = "surrealdb"
    label = "SurrealDB"

    extra_fields = [
        {
            "name": "db_url",
            "type": "str",
            "required": True,
            "order": 1,
            "placeholder": "ws://localhost:8000/rpc",
        },
        {
            "name": "db_username",
            "type": "str",
            "required": True,
            "order": 2,
            "placeholder": "root",
        },
        {
            "name": "db_password",
            "type": "password",
            "required": True,
            "order": 3,
        },
        {
            "name": "db_ns",
            "type": "str",
            "required": True,
            "order": 4,
            "placeholder": "agno",
        },
        {
            "name": "db_db",
            "type": "str",
            "required": True,
            "order": 5,
            "placeholder": "agno",
        },
        *DbBuilder.extra_fields,
    ]

    field_meta = {
        "db_url":      {"label": "数据库 URL", "group": "连接配置", "span": 24},
        "db_username":  {"label": "用户名", "group": "连接配置", "span": 12},
        "db_password":  {"label": "密码", "group": "连接配置", "span": 12},
        "db_ns":       {"label": "命名空间（Namespace）", "group": "连接配置", "span": 12},
        "db_db":       {"label": "数据库名（Database）", "group": "连接配置", "span": 12},
        **DbBuilder.field_meta,
    }

    async def build(self, config: dict, resolver) -> Any:
        from agno.db.surrealdb.surrealdb import SurrealDb

        kwargs = _table_kwargs(config)
        kwargs["db_url"] = config["db_url"]
        kwargs["db_creds"] = {
            "username": config["db_username"],
            "password": config["db_password"],
        }
        kwargs["db_ns"] = config["db_ns"]
        kwargs["db_db"] = config["db_db"]
        kwargs["client"] = None

        return SurrealDb(**kwargs)
