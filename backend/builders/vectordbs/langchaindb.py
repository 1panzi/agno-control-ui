from typing import Any

from builders.vectordbs.base import BaseVectordbBuilder


class LangChainDbBuilder(BaseVectordbBuilder):
    type = "langchaindb"
    label = "LangChain VectorDB"

    # LangChainVectorDb 的构造函数接受 vectorstore 和 knowledge_retriever，
    # 都是运行时 Python 对象，无法通过配置文件传入。
    # 此 Builder 仅用于 schema 注册，build() 不适用于纯配置驱动场景。
    extra_fields: list[dict] = []

    def build(self, config: dict, resolver) -> Any:
        from agno.vectordb.langchaindb import LangChainVectorDb
        return LangChainVectorDb()
