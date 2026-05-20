"""
DynamoDbBuilder — AWS DynamoDB 存储后端。

通过 region_name + AWS 凭证连接，或留空使用环境默认凭证。
"""

from typing import Any

from builders.dbs.base import DbBuilder, _table_kwargs


class DynamoDbBuilder(DbBuilder):
    category = "db"
    type = "dynamo"
    label = "DynamoDB"

    extra_fields = [
        {
            "name": "region_name",
            "type": "str",
            "required": False,
            "order": 1,
            "placeholder": "us-east-1",
        },
        {
            "name": "aws_access_key_id",
            "type": "str",
            "required": False,
            "order": 2,
        },
        {
            "name": "aws_secret_access_key",
            "type": "password",
            "required": False,
            "order": 3,
        },
        *DbBuilder.extra_fields,
    ]

    field_meta = {
        "region_name":            {"label": "AWS 区域", "group": "连接配置", "span": 12},
        "aws_access_key_id":      {"label": "Access Key ID", "group": "连接配置", "span": 12},
        "aws_secret_access_key":  {"label": "Secret Access Key", "group": "连接配置", "span": 24},
        **DbBuilder.field_meta,
    }

    async def build(self, config: dict, resolver) -> Any:
        from agno.db.dynamo.dynamo import DynamoDb

        kwargs = _table_kwargs(config)
        if config.get("region_name"):
            kwargs["region_name"] = config["region_name"]
        if config.get("aws_access_key_id"):
            kwargs["aws_access_key_id"] = config["aws_access_key_id"]
        if config.get("aws_secret_access_key"):
            kwargs["aws_secret_access_key"] = config["aws_secret_access_key"]

        return DynamoDb(**kwargs)
