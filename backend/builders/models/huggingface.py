"""
HuggingFaceModelBuilder — HuggingFace 模型 Builder
"""

from typing import Any

from builders.models.base import BaseModelBuilder


class HuggingFaceModelBuilder(BaseModelBuilder):
    type = "huggingface"
    label = "HuggingFace"
    agno_class = None  # 延迟导入

    extra_fields = [
        *BaseModelBuilder.extra_fields,
        {"name": "temperature", "type": "float", "required": False, "order": 10},
        {"name": "max_tokens", "type": "int", "required": False, "order": 11},
    ]
    field_meta = {
        **BaseModelBuilder.field_meta,
        "model_id": {
            "label": "模型ID",
            "group": "基础配置",
            "span": 12,
            "placeholder": "如 meta-llama/Meta-Llama-3-8B-Instruct",
        },
        "api_key": {
            "label": "HF Token",
            "group": "认证",
            "span": 24,
            "tooltip": "留空则从 HF_TOKEN 环境变量读取",
        },
        "temperature": {
            "label": "温度",
            "group": "生成参数",
            "span": 12,
            "min": 0.0,
            "max": 2.0,
            "step": 0.1,
        },
        "max_tokens": {
            "label": "最大Token",
            "group": "生成参数",
            "span": 12,
            "min": 1,
        },
    }

    def build(self, config: dict, resolver) -> Any:
        from agno.models.huggingface import HuggingFace

        return HuggingFace(
            id=config.get("model_id"),
            api_key=config.get("api_key") or None,
            base_url=config.get("base_url") or None,
            temperature=config.get("temperature"),
            max_tokens=config.get("max_tokens"),
        )
