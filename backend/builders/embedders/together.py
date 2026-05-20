"""
TogetherEmbedderBuilder — Together AI Embedding 模型 Builder
"""

from typing import Any

from builders.embedders.base import BaseEmbedderBuilder


class TogetherEmbedderBuilder(BaseEmbedderBuilder):
    type = "together"
    label = "Together Embedder"
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
            "placeholder": "如 togethercomputer/m2-bert-80M-32k-retrieval",
        },
        "base_url": {
            "label": "Base URL",
            "group": "认证",
            "span": 24,
            "placeholder": "https://api.together.xyz/v1",
        },
    }

    def build(self, config: dict, resolver) -> Any:
        from agno.knowledge.embedder.together import TogetherEmbedder

        kwargs: dict = {
            "id": config.get("model_id"),
        }
        if config.get("api_key"):
            kwargs["api_key"] = config["api_key"]
        if config.get("base_url"):
            kwargs["base_url"] = config["base_url"]
        if config.get("dimensions"):
            kwargs["dimensions"] = config["dimensions"]
        return TogetherEmbedder(**kwargs)
