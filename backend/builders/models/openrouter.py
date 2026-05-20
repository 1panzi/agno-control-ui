"""
OpenRouterModelBuilder — OpenRouter 模型 Builder
"""

from typing import Any

from builders.models.base import BaseModelBuilder


class OpenRouterModelBuilder(BaseModelBuilder):
    type = "openrouter"
    label = "OpenRouter"
    agno_class = None  # 延迟导入

    extra_fields = [
        *BaseModelBuilder.extra_fields,
        {"name": "temperature", "type": "float", "required": False, "default": 0.7, "order": 10},
        {"name": "max_tokens", "type": "int", "required": False, "default": 1024, "order": 11},
    ]
    field_meta = {
        **BaseModelBuilder.field_meta,
        "model_id": {
            "label": "模型ID",
            "group": "基础配置",
            "span": 12,
            "placeholder": "如 openai/gpt-4o / anthropic/claude-3-sonnet",
        },
        "base_url": {
            "label": "Base URL",
            "group": "认证",
            "span": 24,
            "placeholder": "https://openrouter.ai/api/v1",
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
        from agno.models.openrouter import OpenRouter

        return OpenRouter(
            id=config.get("model_id"),
            api_key=config.get("api_key") or None,
            base_url=config.get("base_url") or "https://openrouter.ai/api/v1",
            temperature=config.get("temperature"),
            max_tokens=config.get("max_tokens") or 1024,
        )
