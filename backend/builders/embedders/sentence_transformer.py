"""
SentenceTransformerEmbedderBuilder — SentenceTransformer 本地 Embedding 模型 Builder
"""

from typing import Any

from builders.embedders.base import BaseEmbedderBuilder


class SentenceTransformerEmbedderBuilder(BaseEmbedderBuilder):
    type = "sentence_transformer"
    label = "SentenceTransformer Embedder"
    agno_class = None  # 延迟导入

    extra_fields = [
        {"name": "model_id", "type": "str", "required": True, "order": 1},
        # 本地运行，不需要 api_key / base_url
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
            "placeholder": "如 sentence-transformers/all-MiniLM-L6-v2",
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
        from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder

        kwargs: dict = {
            "id": config.get("model_id"),
        }
        if config.get("dimensions"):
            kwargs["dimensions"] = config["dimensions"]
        return SentenceTransformerEmbedder(**kwargs)
