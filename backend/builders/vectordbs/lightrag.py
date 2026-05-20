from typing import Any

from builders.vectordbs.base import BaseVectordbBuilder


class LightRagBuilder(BaseVectordbBuilder):
    type = "lightrag"
    label = "LightRAG"

    extra_fields = [
        {
            "name": "server_url", "type": "str", "required": False,
            "label": "服务地址", "group": "连接配置", "span": 12, "order": 1,
            "default": "http://localhost:9621",
            "placeholder": "http://localhost:9621",
        },
        {
            "name": "api_key", "type": "password", "required": False,
            "label": "API Key", "group": "连接配置", "span": 12, "order": 2,
        },
    ]

    def build(self, config: dict, resolver) -> Any:
        from agno.vectordb.lightrag import LightRag
        kwargs: dict = {}
        if config.get("server_url"):
            kwargs["server_url"] = config["server_url"]
        if config.get("api_key"):
            kwargs["api_key"] = config["api_key"]
        return LightRag(**kwargs)
