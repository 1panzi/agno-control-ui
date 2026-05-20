from typing import Any

from builders.vectordbs.base import BaseVectordbBuilder


class SingleStoreBuilder(BaseVectordbBuilder):
    type = "singlestore"
    label = "SingleStore"

    extra_fields = [
        {
            "name": "collection", "type": "str", "required": True,
            "label": "集合名", "group": "连接配置", "span": 12, "order": 1,
        },
        {
            "name": "db_url", "type": "password", "required": True,
            "label": "数据库连接串", "group": "连接配置", "span": 24, "order": 2,
            "placeholder": "singlestoredb://user:pass@host:3306/db",
        },
        {
            "name": "schema", "type": "str", "required": False, "default": "ai",
            "label": "Schema", "group": "连接配置", "span": 12, "order": 3,
        },
    ]

    def build(self, config: dict, resolver) -> Any:
        from agno.vectordb.singlestore import SingleStore
        embedder = resolver.resolve(config.get("embedder"))
        kwargs: dict = {
            "collection": config["collection"],
            "db_url": config["db_url"],
            "embedder": embedder,
        }
        if config.get("schema"):
            kwargs["schema"] = config["schema"]
        return SingleStore(**kwargs)
