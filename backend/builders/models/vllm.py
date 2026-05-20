"""
VLLMModelBuilder — vLLM 模型 Builder
"""

from typing import Any

from builders.models.base import BaseModelBuilder


class VLLMModelBuilder(BaseModelBuilder):
    type = "vllm"
    label = "vLLM"
    agno_class = None  # 延迟导入

    extra_fields = [
        {"name": "model_id", "type": "str", "required": True, "order": 1},
        {"name": "api_key", "type": "password", "required": False, "order": 2},
        {"name": "base_url", "type": "str", "required": True, "order": 3},
        {"name": "temperature", "type": "float", "required": False, "default": 0.7, "order": 10},
        {"name": "max_tokens", "type": "int", "required": False, "order": 11},
    ]
    field_meta = {
        **BaseModelBuilder.field_meta,
        "model_id": {
            "label": "模型ID",
            "group": "基础配置",
            "span": 12,
            "placeholder": "vLLM 加载的模型名称",
        },
        "base_url": {
            "label": "vLLM Server URL",
            "group": "认证",
            "span": 24,
            "placeholder": "http://localhost:8000/v1/",
            "required": True,
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
        from agno.models.vllm import VLLM

        return VLLM(
            id=config.get("model_id"),
            api_key=config.get("api_key") or None,
            base_url=config.get("base_url") or None,
            temperature=config.get("temperature") or 0.7,
            max_tokens=config.get("max_tokens"),
        )
