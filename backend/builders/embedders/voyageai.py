"""
VoyageAIEmbedderBuilder — Voyage AI Embedding 模型 Builder
"""

from typing import Any

from builders.embedders.base import BaseEmbedderBuilder


class VoyageAIEmbedderBuilder(BaseEmbedderBuilder):
    type = "voyageai"
    label = "Voyage AI Embedder"
    agno_class = None  # 延迟导入

    extra_fields = [
        {"name": "model_id", "type": "str", "required": True, "order": 1},
        {"name": "api_key", "type": "password", "required": False, "order": 2},
        # VoyageAI 无通用 base_url，隐藏
        {"name": "base_url", "type": "str", "required": False, "order": 3, "hidden": True},
        {"name": "dimensions", "type": "int", "required": False, "order": 4},
    ]
    field_meta = {
        **BaseEmbedderBuilder.field_meta,
        "model_id": {
            "label": "模型ID",
            "group": "基础配置",
            "span": 12,
            "placeholder": "如 voyage-2",
        },
        "base_url": {
            "label": "Base URL",
            "group": "认证",
            "span": 24,
            "hidden": True,
        },
    }

    def build(self, config: dict, resolver) -> Any:
        from agno.knowledge.embedder.voyageai import VoyageAIEmbedder

        kwargs: dict = {
            "id": config.get("model_id"),
        }
        if config.get("api_key"):
            kwargs["api_key"] = config["api_key"]
        if config.get("dimensions"):
            kwargs["dimensions"] = config["dimensions"]
        return VoyageAIEmbedder(**kwargs)
