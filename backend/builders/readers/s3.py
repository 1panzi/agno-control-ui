from typing import Any

from builders.readers.base import BaseReaderBuilder


class S3ReaderBuilder(BaseReaderBuilder):
    type = "s3"
    label = "S3 文件"

    try:
        from agno.knowledge.reader.s3_reader import S3Reader
        agno_class = S3Reader
    except ImportError:
        agno_class = None

    async def build(self, config: dict, resolver) -> Any:
        from agno.knowledge.reader.s3_reader import S3Reader
        chunker = await self._build_chunker(config, resolver)
        kwargs: dict = {
            "chunk": config.get("chunk", True),
            "chunk_size": config.get("chunk_size", 5000),
        }
        if chunker is not None:
            kwargs["chunking_strategy"] = chunker
        return S3Reader(**kwargs)
