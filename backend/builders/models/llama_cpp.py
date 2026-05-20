"""
LlamaCppModelBuilder — Llama.cpp 本地模型 Builder
"""

from typing import Any

from builders.models.base import BaseModelBuilder


class LlamaCppModelBuilder(BaseModelBuilder):
    type = "llama_cpp"
    label = "Llama.cpp"
    agno_class = None  # 延迟导入

    extra_fields = [
        {"name": "model_id", "type": "str", "required": True, "order": 1},
        {"name": "api_key", "type": "password", "required": False, "order": 2, "hidden": True},
        {"name": "base_url", "type": "str", "required": False, "order": 3},
        {"name": "temperature", "type": "float", "required": False, "default": 0.7, "order": 10},
        {"name": "max_tokens", "type": "int", "required": False, "order": 11},
    ]
    field_meta = {
        **BaseModelBuilder.field_meta,
        "model_id": {
            "label": "模型ID",
            "group": "基础配置",
            "span": 12,
            "placeholder": "如 ggml-org/gpt-oss-20b-GGUF",
        },
        "api_key": {"label": "API Key", "group": "认证", "span": 24, "hidden": True},
        "base_url": {
            "label": "Server URL",
            "group": "认证",
            "span": 24,
            "placeholder": "http://127.0.0.1:8080/v1",
        },
        "temperature": {
            "label": "温度",
            "group": "生成参数",
            "span": 12,
            "min": 0.0,
            "max": 2.0,
            "step": 0.1,
            "omit_if_default": True,
        },
        "max_tokens": {
            "label": "最大Token",
            "group": "生成参数",
            "span": 12,
            "min": 1,
        },
    }

    def build(self, config: dict, resolver) -> Any:
        from agno.models.llama_cpp import LlamaCpp

        return LlamaCpp(
            id=config.get("model_id"),
            base_url=config.get("base_url") or "http://127.0.0.1:8080/v1",
            temperature=config.get("temperature"),
            max_tokens=config.get("max_tokens"),
        )
