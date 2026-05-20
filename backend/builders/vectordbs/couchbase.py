from typing import Any

from builders.vectordbs.base import BaseVectordbBuilder


class CouchbaseBuilder(BaseVectordbBuilder):
    type = "couchbase"
    label = "Couchbase"

    extra_fields = [
        {
            "name": "bucket_name", "type": "str", "required": True,
            "label": "Bucket 名", "group": "连接配置", "span": 12, "order": 1,
        },
        {
            "name": "scope_name", "type": "str", "required": True,
            "label": "Scope 名", "group": "连接配置", "span": 12, "order": 2,
        },
        {
            "name": "collection_name", "type": "str", "required": True,
            "label": "集合名", "group": "连接配置", "span": 12, "order": 3,
        },
        {
            "name": "couchbase_connection_string", "type": "str", "required": True,
            "label": "连接串", "group": "连接配置", "span": 24, "order": 4,
            "placeholder": "couchbase://localhost",
        },
        {
            "name": "search_index", "type": "str", "required": True,
            "label": "搜索索引名", "group": "连接配置", "span": 12, "order": 5,
        },
        {
            "name": "username", "type": "str", "required": False,
            "label": "用户名", "group": "连接配置", "span": 12, "order": 6,
        },
        {
            "name": "password", "type": "password", "required": False,
            "label": "密码", "group": "连接配置", "span": 12, "order": 7,
        },
    ]

    def build(self, config: dict, resolver) -> Any:
        from couchbase.options import ClusterOptions
        from couchbase.auth import PasswordAuthenticator
        from agno.vectordb.couchbase import CouchbaseSearch
        embedder = resolver.resolve(config.get("embedder"))
        cluster_options = ClusterOptions(
            PasswordAuthenticator(
                config.get("username", ""),
                config.get("password", ""),
            )
        )
        return CouchbaseSearch(
            bucket_name=config["bucket_name"],
            scope_name=config["scope_name"],
            collection_name=config["collection_name"],
            couchbase_connection_string=config["couchbase_connection_string"],
            cluster_options=cluster_options,
            search_index=config["search_index"],
            embedder=embedder,
        )
