"""
AwsBedrockModelBuilder — AWS Bedrock 模型 Builder
"""

from typing import Any

from builders.models.base import BaseModelBuilder


class AwsBedrockModelBuilder(BaseModelBuilder):
    type = "aws"
    label = "AWS Bedrock"
    agno_class = None  # 延迟导入

    extra_fields = [
        {"name": "model_id", "type": "str", "required": True, "order": 1},
        {"name": "api_key", "type": "password", "required": False, "order": 2, "hidden": True},
        {"name": "base_url", "type": "str", "required": False, "order": 3, "hidden": True},
        {"name": "aws_region", "type": "str", "required": False, "order": 4},
        {"name": "aws_access_key_id", "type": "password", "required": False, "order": 5},
        {"name": "aws_secret_access_key", "type": "password", "required": False, "order": 6},
        {"name": "temperature", "type": "float", "required": False, "order": 10},
        {"name": "max_tokens", "type": "int", "required": False, "order": 11},
    ]
    field_meta = {
        **BaseModelBuilder.field_meta,
        "model_id": {
            "label": "模型ID",
            "group": "基础配置",
            "span": 12,
            "placeholder": "如 anthropic.claude-3-sonnet-20240229-v1:0",
        },
        "api_key": {"label": "API Key", "group": "认证", "span": 24, "hidden": True},
        "base_url": {"label": "Base URL", "group": "认证", "span": 24, "hidden": True},
        "aws_region": {
            "label": "AWS Region",
            "group": "认证",
            "span": 12,
            "placeholder": "如 us-east-1",
            "tooltip": "留空则从 AWS_REGION 环境变量读取",
        },
        "aws_access_key_id": {
            "label": "Access Key ID",
            "group": "认证",
            "span": 12,
            "tooltip": "留空则从 AWS_ACCESS_KEY_ID 环境变量读取",
        },
        "aws_secret_access_key": {
            "label": "Secret Access Key",
            "group": "认证",
            "span": 12,
            "tooltip": "留空则从 AWS_SECRET_ACCESS_KEY 环境变量读取",
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
        from agno.models.aws import AwsBedrock

        return AwsBedrock(
            id=config.get("model_id"),
            aws_region=config.get("aws_region") or None,
            aws_access_key_id=config.get("aws_access_key_id") or None,
            aws_secret_access_key=config.get("aws_secret_access_key") or None,
            temperature=config.get("temperature"),
            max_tokens=config.get("max_tokens"),
        )
