"""
VLLMEmbedderBuilder — vLLM Embedding 模型 Builder（支持本地和远程模式）
"""

from typing import Any

from builders.embedders.base import BaseEmbedderBuilder


class VLLMEmbedderBuilder(BaseEmbedderBuilder):
    type = "vllm"
    label = "vLLM Embedder"
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
            "placeholder": "如 sentence-transformers/all-MiniLM-L6-v2",
        },
        "base_url": {
            "label": "Base URL",
            "group": "认证",
            "span": 24,
            "placeholder": "远程模式填写，如 http://localhost:8000/v1；留空则使用本地模式",
        },
    }

    def build(self, config: dict, resolver) -> Any:
        from agno.knowledge.embedder.vllm import VLLMEmbedder

        kwargs: dict = {
            "id": config.get("model_id"),
        }
        if config.get("api_key"):
            kwargs["api_key"] = config["api_key"]
        if config.get("base_url"):
            kwargs["base_url"] = config["base_url"]
        if config.get("dimensions"):
            kwargs["dimensions"] = config["dimensions"]
        return VLLMEmbedder(**kwargs)
