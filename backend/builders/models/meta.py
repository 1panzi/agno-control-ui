"""
LlamaModelBuilder — Meta Llama 模型 Builder
"""

from typing import Any

from builders.models.base import BaseModelBuilder


class LlamaModelBuilder(BaseModelBuilder):
    type = "meta"
    label = "Meta Llama"
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
            "placeholder": "如 Llama-4-Maverick-17B-128E-Instruct-FP8",
        },
        "api_key": {
            "label": "Llama API Key",
            "group": "认证",
            "span": 24,
            "tooltip": "留空则从 LLAMA_API_KEY 环境变量读取",
        },
        "temperature": {
            "label": "温度",
            "group": "生成参数",
            "span": 12,
            "min": 0.0,
            "max": 2.0,
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
        from agno.models.meta import Llama

        return Llama(
            id=config.get("model_id"),
            api_key=config.get("api_key") or None,
            base_url=config.get("base_url") or None,
            temperature=config.get("temperature"),
            max_completion_tokens=config.get("max_completion_tokens"),
        )
