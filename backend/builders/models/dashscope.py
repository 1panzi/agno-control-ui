"""
DashScopeModelBuilder — DashScope (通义千问) 模型 Builder
"""

from typing import Any

from builders.models.base import BaseModelBuilder


class DashScopeModelBuilder(BaseModelBuilder):
    type = "dashscope"
    label = "DashScope (通义千问)"
    agno_class = None  # 延迟导入

    extra_fields = [
        *BaseModelBuilder.extra_fields,
        {"name": "temperature", "type": "float", "required": False, "default": 0.7, "order": 10},
        {"name": "max_tokens", "type": "int", "required": False, "order": 11},
    ]
    field_meta = {
        **BaseModelBuilder.field_meta,
        "model_id": {
            "label": "模型ID",
            "group": "基础配置",
            "span": 12,
            "placeholder": "如 qwen-plus / qwen-max",
        },
        "api_key": {
            "label": "API Key",
            "group": "认证",
            "span": 24,
            "tooltip": "留空则从 DASHSCOPE_API_KEY 或 QWEN_API_KEY 环境变量读取",
        },
        "base_url": {
            "label": "Base URL",
            "group": "认证",
            "span": 24,
            "placeholder": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
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
        from agno.models.dashscope import DashScope

        return DashScope(
            id=config.get("model_id"),
            api_key=config.get("api_key") or None,
            base_url=config.get("base_url") or "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
            temperature=config.get("temperature"),
            max_tokens=config.get("max_tokens"),
        )
