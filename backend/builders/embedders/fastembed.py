"""
FastEmbedEmbedderBuilder — FastEmbed 本地 Embedding 模型 Builder
"""

from typing import Any

from builders.embedders.base import BaseEmbedderBuilder


class FastEmbedEmbedderBuilder(BaseEmbedderBuilder):
    type = "fastembed"
    label = "FastEmbed Embedder"
    agno_class = None  # 延迟导入

    extra_fields = [
        {"name": "model_id", "type": "str", "required": True, "order": 1},
        # FastEmbed 本地运行，不需要 api_key / base_url
        {"name": "api_key", "type": "password", "required": False, "order": 2, "hidden": True},
        {"name": "base_url", "type": "str", "required": False, "order": 3, "hidden": True},
        {"name": "dimensions", "type": "int", "required": False, "order": 4},
    ]
    field_meta = {
        **BaseEmbedderBuilder.field_meta,
        "model_id": {
            "label": "模型ID",
            "group": "基础配置",
            "span": 12,
            "placeholder": "如 BAAI/bge-small-en-v1.5",
        },
        "api_key": {
            "label": "API Key",
            "group": "认证",
            "span": 24,
            "hidden": True,
        },
        "base_url": {
            "label": "Base URL",
            "group": "认证",
            "span": 24,
            "hidden": True,
        },
    }

    def build(self, config: dict, resolver) -> Any:
        from agno.knowledge.embedder.fastembed import FastEmbedEmbedder

        kwargs: dict = {
            "id": config.get("model_id"),
        }
        if config.get("dimensions"):
            kwargs["dimensions"] = config["dimensions"]
        return FastEmbedEmbedder(**kwargs)
