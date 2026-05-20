from typing import Any

from builders.vectordbs.base import BaseVectordbBuilder


class UpstashBuilder(BaseVectordbBuilder):
    type = "upstashdb"
    label = "Upstash Vector"

    extra_fields = [
        {
            "name": "url", "type": "str", "required": True,
            "label": "Upstash URL", "group": "连接配置", "span": 24, "order": 1,
            "placeholder": "https://xxx.upstash.io",
        },
        {
            "name": "token", "type": "password", "required": True,
            "label": "Token", "group": "连接配置", "span": 24, "order": 2,
        },
        {
            "name": "namespace", "type": "str", "required": False,
            "label": "命名空间", "group": "连接配置", "span": 12, "order": 3,
            "tooltip": "留空使用默认命名空间",
        },
    ]

    def build(self, config: dict, resolver) -> Any:
        from agno.vectordb.upstashdb import UpstashVectorDb
        embedder = resolver.resolve(config.get("embedder"))
        kwargs: dict = {
            "url": config["url"],
            "token": config["token"],
        }
        if embedder is not None:
            kwargs["embedder"] = embedder
        if config.get("namespace"):
            kwargs["namespace"] = config["namespace"]
        return UpstashVectorDb(**kwargs)
