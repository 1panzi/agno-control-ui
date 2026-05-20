"""
AwsBedrockEmbedderBuilder — AWS Bedrock Embedding 模型 Builder
"""

from typing import Any

from builders.embedders.base import BaseEmbedderBuilder


class AwsBedrockEmbedderBuilder(BaseEmbedderBuilder):
    type = "aws_bedrock"
    label = "AWS Bedrock Embedder"
    agno_class = None  # 延迟导入

    extra_fields = [
        {"name": "model_id", "type": "str", "required": True, "order": 1},
        # AWS 不使用通用 api_key / base_url，隐藏
        {"name": "api_key", "type": "password", "required": False, "order": 2, "hidden": True},
        {"name": "base_url", "type": "str", "required": False, "order": 3, "hidden": True},
        {"name": "dimensions", "type": "int", "required": False, "order": 4},
        {"name": "aws_region", "type": "str", "required": False, "order": 5},
        {"name": "aws_access_key_id", "type": "password", "required": False, "order": 6},
        {"name": "aws_secret_access_key", "type": "password", "required": False, "order": 7},
    ]
    field_meta = {
        **BaseEmbedderBuilder.field_meta,
        "model_id": {
            "label": "模型ID",
            "group": "基础配置",
            "span": 12,
            "placeholder": "如 cohere.embed-multilingual-v3 / cohere.embed-v4:0",
        },
        "api_key": {
            "label": "API Key",
            "group": "认证",
            "span": 24,
            "hidden": True,
        },
        "base_url": {
            "label": "Base URL",
            "group": "认证",
            "span": 24,
            "hidden": True,
        },
        "aws_region": {
            "label": "AWS Region",
            "group": "认证",
            "span": 12,
            "placeholder": "如 us-east-1",
        },
        "aws_access_key_id": {
            "label": "Access Key ID",
            "group": "认证",
            "span": 12,
        },
        "aws_secret_access_key": {
            "label": "Secret Access Key",
            "group": "认证",
            "span": 12,
        },
    }

    def build(self, config: dict, resolver) -> Any:
        from agno.knowledge.embedder.aws_bedrock import AwsBedrockEmbedder

        kwargs: dict = {
            "id": config.get("model_id"),
        }
        if config.get("dimensions"):
            kwargs["dimensions"] = config["dimensions"]
        if config.get("aws_region"):
            kwargs["aws_region"] = config["aws_region"]
        if config.get("aws_access_key_id"):
            kwargs["aws_access_key_id"] = config["aws_access_key_id"]
        if config.get("aws_secret_access_key"):
            kwargs["aws_secret_access_key"] = config["aws_secret_access_key"]
        return AwsBedrockEmbedder(**kwargs)
