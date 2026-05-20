from builders.readers.chunk.agentic import AgenticChunkerBuilder
from builders.readers.chunk.base import (
    CHUNKER_REGISTRY,
    BaseChunkerBuilder,
)
from builders.readers.chunk.code import CodeChunkerBuilder
from builders.readers.chunk.document import DocumentChunkerBuilder
from builders.readers.chunk.fixed import FixedSizeChunkerBuilder
from builders.readers.chunk.markdown import MarkdownChunkerBuilder
from builders.readers.chunk.recursive import (
    RecursiveChunkerBuilder,
)
from builders.readers.chunk.row import RowChunkerBuilder
from builders.readers.chunk.semantic import SemanticChunkerBuilder

# 填充注册表
CHUNKER_REGISTRY.update({
    "FixedSizeChunker": FixedSizeChunkerBuilder(),
    "RecursiveChunker": RecursiveChunkerBuilder(),
    "DocumentChunker":  DocumentChunkerBuilder(),
    "MarkdownChunker":  MarkdownChunkerBuilder(),
    "RowChunker":       RowChunkerBuilder(),
    "CodeChunker":      CodeChunkerBuilder(),
    "SemanticChunker":  SemanticChunkerBuilder(),
    "AgenticChunker":   AgenticChunkerBuilder(),
})

__all__ = ["BaseChunkerBuilder", "CHUNKER_REGISTRY"]
