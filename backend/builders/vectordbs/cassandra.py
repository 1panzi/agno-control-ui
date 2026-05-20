from typing import Any

from builders.vectordbs.base import BaseVectordbBuilder


class CassandraBuilder(BaseVectordbBuilder):
    type = "cassandra"
    label = "Cassandra"

    extra_fields = [
        {
            "name": "table_name", "type": "str", "required": True,
            "label": "表名", "group": "连接配置", "span": 12, "order": 1,
        },
        {
            "name": "keyspace", "type": "str", "required": True,
            "label": "Keyspace", "group": "连接配置", "span": 12, "order": 2,
        },
    ]

    def build(self, config: dict, resolver) -> Any:
        from agno.vectordb.cassandra import Cassandra
        embedder = resolver.resolve(config.get("embedder"))
        return Cassandra(
            table_name=config["table_name"],
            keyspace=config["keyspace"],
            embedder=embedder,
        )
