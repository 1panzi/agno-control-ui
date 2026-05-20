"""
VertexAIModelBuilder — Google Vertex AI Claude 模型 Builder
"""

from typing import Any

from builders.models.base import BaseModelBuilder


class VertexAIModelBuilder(BaseModelBuilder):
    type = "vertexai"
    label = "Vertex AI (Claude)"
    agno_class = None  # 延迟导入

    extra_fields = [
        {"name": "model_id", "type": "str", "required": True, "order": 1},
        {"name": "api_key", "type": "password", "required": False, "order": 2, "hidden": True},
        {"name": "base_url", "type": "str", "required": False, "order": 3, "hidden": True},
        {"name": "region", "type": "str", "required": False, "order": 4},
        {"name": "project_id", "type": "str", "required": False, "order": 5},
        {"name": "temperature", "type": "float", "required": False, "order": 10},
        {"name": "max_tokens", "type": "int", "required": False, "order": 11},
    ]
    field_meta = {
        **BaseModelBuilder.field_meta,
        "model_id": {
            "label": "模型ID",
            "group": "基础配置",
            "span": 12,
            "placeholder": "如 claude-sonnet-4@20250514",
        },
        "api_key": {"label": "API Key", "group": "认证", "span": 24, "hidden": True},
        "base_url": {"label": "Base URL", "group": "认证", "span": 24, "hidden": True},
        "region": {
            "label": "Region",
            "group": "认证",
            "span": 12,
            "placeholder": "如 us-east5",
            "tooltip": "留空则从 CLOUD_ML_REGION 环境变量读取",
        },
        "project_id": {
            "label": "Project ID",
            "group": "认证",
            "span": 12,
            "tooltip": "留空则从 ANTHROPIC_VERTEX_PROJECT_ID 环境变量读取",
        },
        "temperature": {
            "label": "温度",
            "group": "生成参数",
            "span": 12,
            "min": 0.0,
            "max": 1.0,
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
        from agno.models.vertexai import Claude

        return Claude(
            id=config.get("model_id"),
            region=config.get("region") or None,
            project_id=config.get("project_id") or None,
            temperature=config.get("temperature"),
            max_tokens=config.get("max_tokens"),
        )
