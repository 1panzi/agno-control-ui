"""
MySQLDbBuilder — MySQL 存储后端。

db_url 为必填项（如 mysql+pymysql://user:pass@host/db）。
"""

from typing import Any

from builders.dbs.base import DbBuilder, _table_kwargs


class MySQLDbBuilder(DbBuilder):
    category = "db"
    type = "mysql"
    label = "MySQL"

    extra_fields = [
        {
            "name": "db_url",
            "type": "str",
            "required": True,
            "order": 1,
            "placeholder": "mysql+pymysql://user:pass@host:3306/dbname",
        },
        {
            "name": "db_schema",
            "type": "str",
            "required": False,
            "order": 2,
            "placeholder": "agno（留空使用默认 schema）",
        },
        {
            "name": "create_schema",
            "type": "bool",
            "required": False,
            "default": True,
            "order": 3,
        },
        *DbBuilder.extra_fields,
    ]

    field_meta = {
        "db_url":        {"label": "数据库 URL", "group": "连接配置", "span": 24},
        "db_schema":     {"label": "Schema 名", "group": "连接配置", "span": 12,
                          "tooltip": "MySQL schema，留空使用 agno 默认"},
        "create_schema": {"label": "自动创建 Schema", "group": "连接配置", "span": 12},
        **DbBuilder.field_meta,
    }

    async def build(self, config: dict, resolver) -> Any:
        from agno.db.mysql.mysql import MySQLDb

        kwargs = _table_kwargs(config)
        if config.get("db_url"):
            kwargs["db_url"] = config["db_url"]
        if config.get("db_schema"):
            kwargs["db_schema"] = config["db_schema"]
        kwargs["create_schema"] = config.get("create_schema", True)

        return MySQLDb(**kwargs)
