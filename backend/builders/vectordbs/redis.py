from typing import Any

from builders.vectordbs.base import BaseVectordbBuilder


class RedisBuilder(BaseVectordbBuilder):
    type = "redis"
    label = "Redis"

    extra_fields = [
        {
            "name": "index_name", "type": "str", "required": True,
            "label": "索引名", "group": "连接配置", "span": 12, "order": 1,
        },
        {
            "name": "redis_url", "type": "password", "required": True,
            "label": "Redis URL", "group": "连接配置", "span": 24, "order": 2,
            "placeholder": "redis://localhost:6379",
        },
    ]

    def build(self, config: dict, resolver) -> Any:
        from agno.vectordb.redis import RedisDB
        embedder = resolver.resolve(config.get("embedder"))
        return RedisDB(
            index_name=config["index_name"],
            redis_url=config["redis_url"],
            embedder=embedder,
        )
