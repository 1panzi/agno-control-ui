from typing import Any

from builders.vectordbs.base import BaseVectordbBuilder


class ClickhouseBuilder(BaseVectordbBuilder):
    type = "clickhouse"
    label = "ClickHouse"

    extra_fields = [
        {
            "name": "table_name", "type": "str", "required": True,
            "label": "表名", "group": "连接配置", "span": 12, "order": 1,
        },
        {
            "name": "host", "type": "str", "required": True,
            "label": "服务地址", "group": "连接配置", "span": 12, "order": 2,
            "placeholder": "localhost",
        },
        {
            "name": "port", "type": "int", "required": False, "default": 0,
            "label": "端口", "group": "连接配置", "span": 12, "order": 3,
            "tooltip": "留空使用默认端口",
        },
        {
            "name": "username", "type": "str", "required": False,
            "label": "用户名", "group": "连接配置", "span": 12, "order": 4,
        },
        {
            "name": "password", "type": "password", "required": False,
            "label": "密码", "group": "连接配置", "span": 12, "order": 5,
        },
        {
            "name": "database_name", "type": "str", "required": False, "default": "ai",
            "label": "数据库名", "group": "连接配置", "span": 12, "order": 6,
        },
    ]

    def build(self, config: dict, resolver) -> Any:
        from agno.vectordb.clickhouse import Clickhouse
        embedder = resolver.resolve(config.get("embedder"))
        kwargs: dict = {
            "table_name": config["table_name"],
            "host": config["host"],
            "embedder": embedder,
        }
        if config.get("port"):
            kwargs["port"] = config["port"]
        if config.get("username"):
            kwargs["username"] = config["username"]
        if config.get("password"):
            kwargs["password"] = config["password"]
        if config.get("database_name"):
            kwargs["database_name"] = config["database_name"]
        return Clickhouse(**kwargs)
