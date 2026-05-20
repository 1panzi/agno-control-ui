"""
NebiusEmbedderBuilder — Nebius Embedding 模型 Builder
"""

from typing import Any

from builders.embedders.base import BaseEmbedderBuilder


class NebiusEmbedderBuilder(BaseEmbedderBuilder):
    type = "nebius"
    label = "Nebius Embedder"
    agno_class = None  # 延迟导入

    extra_fields = [
        *BaseEmbedderBuilder.extra_fields,
    ]
    field_meta = {
        **BaseEmbedderBuilder.field_meta,
        "model_id": {
            "label": "模型ID",
            "group": "基础配置",
            "span": 12,
            "placeholder": "如 BAAI/bge-en-icl",
        },
        "base_url": {
            "label": "Base URL",
            "group": "认证",
            "span": 24,
            "placeholder": "https://api.tokenfactory.nebius.com/v1/",
        },
    }

    def build(self, config: dict, resolver) -> Any:
        from agno.knowledge.embedder.nebius import NebiusEmbedder

        kwargs: dict = {
            "id": config.get("model_id"),
        }
        if config.get("api_key"):
            kwargs["api_key"] = config["api_key"]
        if config.get("base_url"):
            kwargs["base_url"] = config["base_url"]
        if config.get("dimensions"):
            kwargs["dimensions"] = config["dimensions"]
        return NebiusEmbedder(**kwargs)
