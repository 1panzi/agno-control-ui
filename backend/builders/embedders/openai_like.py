"""
OpenAILikeEmbedderBuilder — OpenAI 兼容 Embedding 模型 Builder
"""

from typing import Any

from builders.embedders.base import BaseEmbedderBuilder


class OpenAILikeEmbedderBuilder(BaseEmbedderBuilder):
    type = "openai_like"
    label = "OpenAI-Like Embedder"
    agno_class = None  # 延迟导入

    extra_fields = [
        {"name": "model_id", "type": "str", "required": True, "order": 1},
        {"name": "api_key", "type": "password", "required": False, "order": 2},
        {"name": "base_url", "type": "str", "required": True, "order": 3},
        {"name": "dimensions", "type": "int", "required": False, "order": 4},
    ]
    field_meta = {
        **BaseEmbedderBuilder.field_meta,
        "model_id": {
            "label": "模型ID",
            "group": "基础配置",
            "span": 12,
            "placeholder": "提供商的嵌入模型ID",
        },
        "base_url": {
            "label": "Base URL",
            "group": "认证",
            "span": 24,
            "placeholder": "OpenAI 兼容的 /v1/embeddings 端点",
            "required": True,
        },
    }

    def build(self, config: dict, resolver) -> Any:
        from agno.knowledge.embedder.openai_like import OpenAILikeEmbedder

        kwargs: dict = {
            "id": config.get("model_id"),
        }
        if config.get("api_key"):
            kwargs["api_key"] = config["api_key"]
        if config.get("base_url"):
            kwargs["base_url"] = config["base_url"]
        if config.get("dimensions"):
            kwargs["dimensions"] = config["dimensions"]
        return OpenAILikeEmbedder(**kwargs)
