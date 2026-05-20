from typing import Any

from builders.vectordbs.base import BaseVectordbBuilder


class LlamaIndexBuilder(BaseVectordbBuilder):
    type = "llamaindex"
    label = "LlamaIndex VectorDB"

    # LlamaIndexVectorDb 的构造函数接受 knowledge_retriever（运行时 Python 对象），
    # 无法通过配置文件传入。此 Builder 仅用于 schema 注册。
    extra_fields: list[dict] = []

    def build(self, config: dict, resolver) -> Any:
        raise NotImplementedError(
            "LlamaIndex VectorDB 需要传入 knowledge_retriever 实例，无法通过纯配置构建"
        )
