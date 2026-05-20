"""
GoogleModelBuilder — Google Gemini 模型 Builder
"""

from typing import Any

from builders.models.base import BaseModelBuilder


class GoogleModelBuilder(BaseModelBuilder):
    type = "google"
    label = "Google Gemini"
    agno_class = None  # 延迟导入

    extra_fields = [
        *BaseModelBuilder.extra_fields,
        {"name": "temperature", "type": "float", "required": False, "order": 10},
        {"name": "max_output_tokens", "type": "int", "required": False, "order": 11},
    ]
    field_meta = {
        **BaseModelBuilder.field_meta,
        "model_id": {
            "label": "模型ID",
            "group": "基础配置",
            "span": 12,
            "placeholder": "如 gemini-2.5-flash / gemini-2.5-pro",
        },
        "api_key": {
            "label": "Google API Key",
            "group": "认证",
            "span": 24,
            "tooltip": "留空则从 GOOGLE_API_KEY 环境变量读取",
        },
        "base_url": {
            "label": "Base URL",
            "group": "认证",
            "span": 24,
            "hidden": True,
        },
        "temperature": {
            "label": "温度",
            "group": "生成参数",
            "span": 12,
            "min": 0.0,
            "max": 2.0,
            "step": 0.1,
        },
        "max_output_tokens": {
            "label": "最大输出Token",
            "group": "生成参数",
            "span": 12,
            "min": 1,
        },
    }

    def build(self, config: dict, resolver) -> Any:
        from agno.models.google import Gemini

        return Gemini(
            id=config.get("model_id"),
            api_key=config.get("api_key") or None,
            temperature=config.get("temperature"),
            max_output_tokens=config.get("max_output_tokens"),
        )
