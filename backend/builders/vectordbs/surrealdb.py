from typing import Any

from builders.vectordbs.base import BaseVectordbBuilder


class SurrealDbBuilder(BaseVectordbBuilder):
    type = "surrealdb"
    label = "SurrealDB"

    extra_fields = [
        {
            "name": "collection", "type": "str", "required": False, "default": "documents",
            "label": "集合名", "group": "连接配置", "span": 12, "order": 1,
        },
        {
            "name": "url", "type": "str", "required": True,
            "label": "服务地址", "group": "连接配置", "span": 12, "order": 2,
            "placeholder": "ws://localhost:8000",
        },
        {
            "name": "namespace", "type": "str", "required": False,
            "label": "命名空间", "group": "连接配置", "span": 12, "order": 3,
        },
        {
            "name": "database", "type": "str", "required": False,
            "label": "数据库名", "group": "连接配置", "span": 12, "order": 4,
        },
        {
            "name": "username", "type": "str", "required": False,
            "label": "用户名", "group": "连接配置", "span": 12, "order": 5,
        },
        {
            "name": "password", "type": "password", "required": False,
            "label": "密码", "group": "连接配置", "span": 12, "order": 6,
        },
    ]

    def build(self, config: dict, resolver) -> Any:
        from surrealdb import BlockingWsSurrealConnection
        from agno.vectordb.surrealdb import SurrealDb
        embedder = resolver.resolve(config.get("embedder"))
        url = config["url"]
        client = BlockingWsSurrealConnection(url)
        if config.get("namespace") and config.get("database"):
            client.use(config["namespace"], config["database"])
        if config.get("username") and config.get("password"):
            client.signin({"username": config["username"], "password": config["password"]})
        kwargs: dict = {
            "client": client,
            "collection": config.get("collection", "documents"),
            "embedder": embedder,
        }
        return SurrealDb(**kwargs)
