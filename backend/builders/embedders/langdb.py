"""
LangDBEmbedderBuilder — LangDB Embedding 模型 Builder
"""

from typing import Any

from builders.embedders.base import BaseEmbedderBuilder


class LangDBEmbedderBuilder(BaseEmbedderBuilder):
    type = "langdb"
    label = "LangDB Embedder"
    agno_class = None  # 延迟导入

    extra_fields = [
        {"name": "model_id", "type": "str", "required": True, "order": 1},
        {"name": "api_key", "type": "password", "required": False, "order": 2},
        {"name": "base_url", "type": "str", "required": False, "order": 3},
        {"name": "dimensions", "type": "int", "required": False, "order": 4},
        {"name": "project_id", "type": "str", "required": True, "order": 5},
    ]
    field_meta = {
        **BaseEmbedderBuilder.field_meta,
        "model_id": {
            "label": "模型ID",
            "group": "基础配置",
            "span": 12,
            "placeholder": "如 text-embedding-ada-002",
        },
        "project_id": {
            "label": "Project ID",
            "group": "认证",
            "span": 24,
            "tooltip": "LangDB 项目ID，用于构建 API 端点",
        },
        "base_url": {
            "label": "Base URL",
            "group": "认证",
            "span": 24,
            "placeholder": "留空则自动根据 Project ID 生成",
        },
    }

    def build(self, config: dict, resolver) -> Any:
        from agno.knowledge.embedder.langdb import LangDBEmbedder

        kwargs: dict = {
            "id": config.get("model_id"),
        }
        if config.get("api_key"):
            kwargs["api_key"] = config["api_key"]
        if config.get("project_id"):
            kwargs["project_id"] = config["project_id"]
        if config.get("base_url"):
            kwargs["base_url"] = config["base_url"]
        if config.get("dimensions"):
            kwargs["dimensions"] = config["dimensions"]
        return LangDBEmbedder(**kwargs)
