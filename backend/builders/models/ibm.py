"""
WatsonXModelBuilder — IBM WatsonX 模型 Builder
"""

from typing import Any

from builders.models.base import BaseModelBuilder


class WatsonXModelBuilder(BaseModelBuilder):
    type = "ibm"
    label = "IBM WatsonX"
    agno_class = None  # 延迟导入

    extra_fields = [
        {"name": "model_id", "type": "str", "required": True, "order": 1},
        {"name": "api_key", "type": "password", "required": False, "order": 2},
        {"name": "base_url", "type": "str", "required": False, "order": 3},
        {"name": "project_id", "type": "str", "required": False, "order": 4},
        {"name": "temperature", "type": "float", "required": False, "order": 10},
        {"name": "max_tokens", "type": "int", "required": False, "order": 11},
    ]
    field_meta = {
        **BaseModelBuilder.field_meta,
        "model_id": {
            "label": "模型ID",
            "group": "基础配置",
            "span": 12,
            "placeholder": "如 ibm/granite-20b-code-instruct",
        },
        "api_key": {
            "label": "API Key",
            "group": "认证",
            "span": 24,
            "tooltip": "留空则从 IBM_WATSONX_API_KEY 环境变量读取",
        },
        "base_url": {
            "label": "URL",
            "group": "认证",
            "span": 24,
            "placeholder": "https://eu-de.ml.cloud.ibm.com",
            "tooltip": "留空则从 IBM_WATSONX_URL 环境变量读取",
        },
        "project_id": {
            "label": "Project ID",
            "group": "认证",
            "span": 12,
            "tooltip": "留空则从 IBM_WATSONX_PROJECT_ID 环境变量读取",
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
        from agno.models.ibm import WatsonX

        return WatsonX(
            id=config.get("model_id"),
            api_key=config.get("api_key") or None,
            url=config.get("base_url") or None,
            project_id=config.get("project_id") or None,
            temperature=config.get("temperature"),
            max_tokens=config.get("max_tokens"),
        )
