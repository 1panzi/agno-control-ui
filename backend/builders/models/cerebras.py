"""
CerebrasModelBuilder — Cerebras 模型 Builder
"""

from typing import Any

from builders.models.base import BaseModelBuilder


class CerebrasModelBuilder(BaseModelBuilder):
    type = "cerebras"
    label = "Cerebras"
    agno_class = None  # 延迟导入

    extra_fields = [
        *BaseModelBuilder.extra_fields,
        {"name": "temperature", "type": "float", "required": False, "order": 10},
        {"name": "max_completion_tokens", "type": "int", "required": False, "order": 11},
    ]
    field_meta = {
        **BaseModelBuilder.field_meta,
        "model_id": {
            "label": "模型ID",
            "group": "基础配置",
            "span": 12,
            "placeholder": "如 llama-4-scout-17b-16e-instruct",
        },
        "temperature": {
            "label": "温度",
            "group": "生成参数",
            "span": 12,
            "min": 0.0,
            "max": 1.5,
            "step": 0.1,
        },
        "max_completion_tokens": {
            "label": "最大Token",
            "group": "生成参数",
            "span": 12,
            "min": 1,
        },
    }

    def build(self, config: dict, resolver) -> Any:
        from agno.models.cerebras import Cerebras

        return Cerebras(
            id=config.get("model_id"),
            api_key=config.get("api_key") or None,
            base_url=config.get("base_url") or None,
            temperature=config.get("temperature"),
            max_completion_tokens=config.get("max_completion_tokens"),
        )
