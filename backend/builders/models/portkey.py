"""
PortkeyModelBuilder — Portkey AI Gateway 模型 Builder
"""

from typing import Any

from builders.models.base import BaseModelBuilder


class PortkeyModelBuilder(BaseModelBuilder):
    type = "portkey"
    label = "Portkey"
    agno_class = None  # 延迟导入

    extra_fields = [
        {"name": "model_id", "type": "str", "required": True, "order": 1},
        {"name": "api_key", "type": "password", "required": True, "order": 2},
        {"name": "base_url", "type": "str", "required": False, "order": 3, "hidden": True},
        {"name": "virtual_key", "type": "str", "required": False, "order": 4},
        {"name": "temperature", "type": "float", "required": False, "default": 0.7, "order": 10},
        {"name": "max_tokens", "type": "int", "required": False, "order": 11},
    ]
    field_meta = {
        **BaseModelBuilder.field_meta,
        "model_id": {
            "label": "模型ID",
            "group": "基础配置",
            "span": 12,
            "placeholder": "如 gpt-4o-mini",
        },
        "api_key": {
            "label": "Portkey API Key",
            "group": "认证",
            "span": 24,
            "tooltip": "Portkey API Key（必填）",
        },
        "base_url": {"label": "Base URL", "group": "认证", "span": 24, "hidden": True},
        "virtual_key": {
            "label": "Virtual Key",
            "group": "认证",
            "span": 24,
            "tooltip": "留空则从 PORTKEY_VIRTUAL_KEY 环境变量读取",
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
        from agno.models.portkey import Portkey

        return Portkey(
            id=config.get("model_id"),
            portkey_api_key=config.get("api_key") or None,
            virtual_key=config.get("virtual_key") or None,
            temperature=config.get("temperature"),
            max_tokens=config.get("max_tokens"),
        )
