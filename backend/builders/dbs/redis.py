"""
RedisDbBuilder — Redis 存储后端。

通过 db_url 连接 Redis，支持 key 前缀和 TTL 配置。
"""

from typing import Any

from builders.dbs.base import DbBuilder, _table_kwargs


class RedisDbBuilder(DbBuilder):
    category = "db"
    type = "redis"
    label = "Redis"

    extra_fields = [
        {
            "name": "db_url",
            "type": "str",
            "required": True,
            "order": 1,
            "placeholder": "redis://localhost:6379/0",
        },
        {
            "name": "db_prefix",
            "type": "str",
            "required": False,
            "order": 2,
            "default": "agno",
            "placeholder": "agno",
        },
        {
            "name": "expire",
            "type": "int",
            "required": False,
            "order": 3,
            "placeholder": "TTL 秒数（留空不过期）",
        },
        *DbBuilder.extra_fields,
    ]

    field_meta = {
        "db_url":    {"label": "Redis URL", "group": "连接配置", "span": 24},
        "db_prefix": {"label": "Key 前缀", "group": "连接配置", "span": 12,
                      "tooltip": "所有 Redis key 的前缀，默认 agno"},
        "expire":    {"label": "过期时间（秒）", "group": "连接配置", "span": 12,
                      "tooltip": "Redis key 的 TTL，留空表示不过期"},
        **DbBuilder.field_meta,
    }

    async def build(self, config: dict, resolver) -> Any:
        from agno.db.redis.redis import RedisDb

        kwargs = _table_kwargs(config)
        if config.get("db_url"):
            kwargs["db_url"] = config["db_url"]
        if config.get("db_prefix"):
            kwargs["db_prefix"] = config["db_prefix"]
        if config.get("expire"):
            kwargs["expire"] = config["expire"]

        return RedisDb(**kwargs)
