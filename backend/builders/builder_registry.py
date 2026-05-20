"""
全局 Builder 注册表。

key = (category, type) tuple
value = BaseBuilder 实例

- Reader: 每种类型独立 Builder 文件，BaseReaderBuilder 负责 chunking schema 动态生成
- Toolkit: GenericToolkitBuilder 按 catalog 懒加载（100+ agno 工具，不逐一写 Builder）
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from builders.builder_base import BaseBuilder

# ── Model Builders ──────────────────────────────────────────────────────────
# ── Agent Builders ───────────────────────────────────────────────────────────
from .agents.base import AgentBuilder

# ── Compress Builders ─────────────────────────────────────────────────────────
from .compress.base import CompressionManagerBuilder

# ── Culture Builders ──────────────────────────────────────────────────────────
from .culture.base import CultureManagerBuilder
from .embedders.aws_bedrock import AwsBedrockEmbedderBuilder
from .embedders.azure import AzureEmbedderBuilder
from .embedders.cohere import CohereEmbedderBuilder
from .embedders.fastembed import FastEmbedEmbedderBuilder
from .embedders.fireworks import FireworksEmbedderBuilder
from .embedders.google import GoogleEmbedderBuilder
from .embedders.huggingface import HuggingfaceEmbedderBuilder
from .embedders.jina import JinaEmbedderBuilder
from .embedders.langdb import LangDBEmbedderBuilder
from .embedders.mistral import MistralEmbedderBuilder
from .embedders.nebius import NebiusEmbedderBuilder
from .embedders.ollama import OllamaEmbedderBuilder
from .embedders.openai_like import OpenAILikeEmbedderBuilder

# ── Embedder Builders ────────────────────────────────────────────────────────
from .embedders.openai import OpenAIEmbedderBuilder
from .embedders.sentence_transformer import SentenceTransformerEmbedderBuilder
from .embedders.together import TogetherEmbedderBuilder
from .embedders.vllm import VLLMEmbedderBuilder
from .embedders.voyageai import VoyageAIEmbedderBuilder

# ── Guardrail Builders ────────────────────────────────────────────────────────
from .guardrails.base import (
    OpenAIModerationGuardrailBuilder,
    PIIDetectionGuardrailBuilder,
    PromptInjectionGuardrailBuilder,
)

# ── Knowledge Builders ───────────────────────────────────────────────────────
from .knowledge.base import KnowledgeBuilder

# ── Learn Builders ────────────────────────────────────────────────────────────
from .learn.base import LearningMachineBuilder

# ── Memory Builders ───────────────────────────────────────────────────────────
from .memory.base import MemoryManagerBuilder
from .models.aimlapi import AIMLAPIModelBuilder
from .models.anthropic import AnthropicModelBuilder
from .models.aws import AwsBedrockModelBuilder
from .models.azure import AzureModelBuilder
from .models.cerebras import CerebrasModelBuilder
from .models.cohere import CohereModelBuilder
from .models.cometapi import CometAPIModelBuilder
from .models.dashscope import DashScopeModelBuilder
from .models.deepinfra import DeepInfraModelBuilder
from .models.deepseek import DeepSeekModelBuilder
from .models.fireworks import FireworksModelBuilder
from .models.google import GoogleModelBuilder
from .models.groq import GroqModelBuilder
from .models.huggingface import HuggingFaceModelBuilder
from .models.ibm import WatsonXModelBuilder
from .models.internlm import InternLMModelBuilder
from .models.langdb import LangDBModelBuilder
from .models.litellm import LiteLLMModelBuilder
from .models.llama_cpp import LlamaCppModelBuilder
from .models.lmstudio import LMStudioModelBuilder
from .models.meta import LlamaModelBuilder
from .models.mistral import MistralModelBuilder
from .models.moonshot import MoonshotModelBuilder
from .models.n1n import N1NModelBuilder
from .models.nebius import NebiusModelBuilder
from .models.neosantara import NeosantaraModelBuilder
from .models.nexus import NexusModelBuilder
from .models.nvidia import NvidiaModelBuilder
from .models.ollama import OllamaModelBuilder
from .models.openai import OpenAIModelBuilder
from .models.openai_like import OpenAILikeModelBuilder
from .models.openrouter import OpenRouterModelBuilder
from .models.perplexity import PerplexityModelBuilder
from .models.portkey import PortkeyModelBuilder
from .models.requesty import RequestyModelBuilder
from .models.sambanova import SambaNovaModelBuilder
from .models.siliconflow import SiliconFlowModelBuilder
from .models.together import TogetherModelBuilder
from .models.vertexai import VertexAIModelBuilder
from .models.vllm import VLLMModelBuilder
from .models.xai import XAIModelBuilder
from .readers.arxiv import ArxivReaderBuilder
from .readers.csv import CsvReaderBuilder
from .readers.docling import DoclingReaderBuilder
from .readers.docx import DocxReaderBuilder
from .readers.excel import ExcelReaderBuilder
from .readers.field_labeled_csv import FieldLabeledCsvReaderBuilder
from .readers.firecrawl import FirecrawlReaderBuilder
from .readers.json_reader import JsonReaderBuilder
from .readers.llms_txt import LlmsTxtReaderBuilder
from .readers.markdown import MarkdownReaderBuilder

# ── Reader Builders ───────────────────────────────────────────────────────────
from .readers.pdf import PdfReaderBuilder
from .readers.pptx import PptxReaderBuilder
from .readers.s3 import S3ReaderBuilder
from .readers.tavily import TavilyReaderBuilder
from .readers.text import TextReaderBuilder
from .readers.web_search import WebSearchReaderBuilder
from .readers.website import WebsiteReaderBuilder
from .readers.wikipedia import WikipediaReaderBuilder
from .readers.youtube import YoutubeReaderBuilder

# ── Reasoning Builders ────────────────────────────────────────────────────────
from .reasoning.base import ReasoningBuilder

# ── SessionSummary Builders ───────────────────────────────────────────────────
from .session_summary.base import (
    SessionSummaryManagerBuilder,
)

# ── Skill Builders ────────────────────────────────────────────────────────────
from .skills.base import SkillBuilder

# ── Team Builders ────────────────────────────────────────────────────────────
from .teams.base import TeamBuilder

# ── Toolkit Builders (Catalog-based) ─────────────────────────────────────────
from .toolkits.catalog import TOOLKIT_CATALOG
from .toolkits.custom import CustomToolkitBuilder
from .toolkits.generic import GenericToolkitBuilder
from .vectordbs.cassandra import CassandraBuilder
from .vectordbs.chroma import ChromaBuilder
from .vectordbs.clickhouse import ClickhouseBuilder
from .vectordbs.couchbase import CouchbaseBuilder
from .vectordbs.lancedb import LanceDbBuilder
from .vectordbs.langchaindb import LangChainDbBuilder
from .vectordbs.lightrag import LightRagBuilder
from .vectordbs.llamaindex import LlamaIndexBuilder
from .vectordbs.milvus import MilvusBuilder
from .vectordbs.mongodb import MongodbBuilder
from .vectordbs.redis import RedisBuilder
from .vectordbs.singlestore import SingleStoreBuilder
from .vectordbs.surrealdb import SurrealDbBuilder
from .vectordbs.upstashdb import UpstashBuilder

# ── DB Builders ──────────────────────────────────────────────────────────────
from .dbs.async_postgres import AsyncPostgresDbBuilder
from .dbs.dynamo import DynamoDbBuilder
from .dbs.firestore import FirestoreDbBuilder
from .dbs.gcs_json import GcsJsonDbBuilder
from .dbs.in_memory import InMemoryDbBuilder
from .dbs.json_db import JsonDbBuilder
from .dbs.mongo import MongoDbBuilder
from .dbs.mysql import MySQLDbBuilder
from .dbs.postgres import PostgresDbBuilder
from .dbs.redis import RedisDbBuilder as RedisDbBuilderDb
from .dbs.singlestore import SingleStoreDbBuilder as SingleStoreDbBuilderDb
from .dbs.sqlite import SqliteDbBuilder
from .dbs.surrealdb import SurrealDbBuilder as SurrealDbBuilderDb

# ── VectorDB Builders ────────────────────────────────────────────────────────
from .vectordbs.pgvector import PgVectorBuilder
from .vectordbs.pinecone import PineconeBuilder
from .vectordbs.qdrant import QdrantBuilder
from .vectordbs.weaviate import WeaviateBuilder

# ── 注册表 ────────────────────────────────────────────────────────────────────
builder_registry: dict[tuple[str, str], "BaseBuilder"] = {
    # models
    ("model", "openai"):      OpenAIModelBuilder(),
    ("model", "anthropic"):   AnthropicModelBuilder(),
    ("model", "ollama"):      OllamaModelBuilder(),
    ("model", "groq"):        GroqModelBuilder(),
    ("model", "deepseek"):    DeepSeekModelBuilder(),
    ("model", "mistral"):     MistralModelBuilder(),
    ("model", "azure"):       AzureModelBuilder(),
    ("model", "cohere"):      CohereModelBuilder(),
    ("model", "together"):    TogetherModelBuilder(),
    ("model", "openai_like"): OpenAILikeModelBuilder(),
    ("model", "google"):      GoogleModelBuilder(),
    ("model", "aws"):         AwsBedrockModelBuilder(),
    ("model", "huggingface"): HuggingFaceModelBuilder(),
    ("model", "litellm"):     LiteLLMModelBuilder(),
    ("model", "fireworks"):   FireworksModelBuilder(),
    ("model", "cerebras"):    CerebrasModelBuilder(),
    ("model", "nvidia"):      NvidiaModelBuilder(),
    ("model", "vertexai"):    VertexAIModelBuilder(),
    ("model", "openrouter"):  OpenRouterModelBuilder(),
    ("model", "perplexity"):  PerplexityModelBuilder(),
    ("model", "xai"):         XAIModelBuilder(),
    ("model", "sambanova"):   SambaNovaModelBuilder(),
    ("model", "siliconflow"): SiliconFlowModelBuilder(),
    ("model", "dashscope"):   DashScopeModelBuilder(),
    ("model", "moonshot"):    MoonshotModelBuilder(),
    ("model", "deepinfra"):   DeepInfraModelBuilder(),
    ("model", "ibm"):         WatsonXModelBuilder(),
    ("model", "meta"):        LlamaModelBuilder(),
    ("model", "vllm"):        VLLMModelBuilder(),
    ("model", "llama_cpp"):   LlamaCppModelBuilder(),
    ("model", "lmstudio"):    LMStudioModelBuilder(),
    ("model", "internlm"):    InternLMModelBuilder(),
    ("model", "nebius"):      NebiusModelBuilder(),
    ("model", "portkey"):     PortkeyModelBuilder(),
    ("model", "aimlapi"):     AIMLAPIModelBuilder(),
    ("model", "cometapi"):    CometAPIModelBuilder(),
    ("model", "langdb"):      LangDBModelBuilder(),
    ("model", "n1n"):         N1NModelBuilder(),
    ("model", "neosantara"):  NeosantaraModelBuilder(),
    ("model", "nexus"):       NexusModelBuilder(),
    ("model", "requesty"):    RequestyModelBuilder(),
    # embedders
    ("embedder", "openai"):               OpenAIEmbedderBuilder(),
    ("embedder", "azure"):                AzureEmbedderBuilder(),
    ("embedder", "ollama"):               OllamaEmbedderBuilder(),
    ("embedder", "cohere"):               CohereEmbedderBuilder(),
    ("embedder", "google"):               GoogleEmbedderBuilder(),
    ("embedder", "aws_bedrock"):          AwsBedrockEmbedderBuilder(),
    ("embedder", "fireworks"):            FireworksEmbedderBuilder(),
    ("embedder", "huggingface"):          HuggingfaceEmbedderBuilder(),
    ("embedder", "jina"):                 JinaEmbedderBuilder(),
    ("embedder", "mistral"):              MistralEmbedderBuilder(),
    ("embedder", "nebius"):               NebiusEmbedderBuilder(),
    ("embedder", "openai_like"):          OpenAILikeEmbedderBuilder(),
    ("embedder", "together"):             TogetherEmbedderBuilder(),
    ("embedder", "fastembed"):            FastEmbedEmbedderBuilder(),
    ("embedder", "sentence_transformer"): SentenceTransformerEmbedderBuilder(),
    ("embedder", "vllm"):                 VLLMEmbedderBuilder(),
    ("embedder", "voyageai"):             VoyageAIEmbedderBuilder(),
    ("embedder", "langdb"):               LangDBEmbedderBuilder(),
    # vectordbs
    ("vectordb", "pgvector"):     PgVectorBuilder(),
    ("vectordb", "qdrant"):       QdrantBuilder(),
    ("vectordb", "chroma"):       ChromaBuilder(),
    ("vectordb", "pinecone"):     PineconeBuilder(),
    ("vectordb", "weaviate"):     WeaviateBuilder(),
    ("vectordb", "milvus"):       MilvusBuilder(),
    ("vectordb", "mongodb"):      MongodbBuilder(),
    ("vectordb", "lancedb"):      LanceDbBuilder(),
    ("vectordb", "cassandra"):    CassandraBuilder(),
    ("vectordb", "clickhouse"):   ClickhouseBuilder(),
    ("vectordb", "couchbase"):    CouchbaseBuilder(),
    ("vectordb", "langchaindb"):  LangChainDbBuilder(),
    ("vectordb", "lightrag"):     LightRagBuilder(),
    ("vectordb", "llamaindex"):   LlamaIndexBuilder(),
    ("vectordb", "redis"):        RedisBuilder(),
    ("vectordb", "singlestore"):  SingleStoreBuilder(),
    ("vectordb", "surrealdb"):    SurrealDbBuilder(),
    ("vectordb", "upstashdb"):    UpstashBuilder(),
    # readers
    ("reader", "pdf"):              PdfReaderBuilder(),
    ("reader", "docx"):             DocxReaderBuilder(),
    ("reader", "text"):             TextReaderBuilder(),
    ("reader", "csv"):              CsvReaderBuilder(),
    ("reader", "json"):             JsonReaderBuilder(),
    ("reader", "website"):          WebsiteReaderBuilder(),
    ("reader", "youtube"):          YoutubeReaderBuilder(),
    ("reader", "arxiv"):            ArxivReaderBuilder(),
    ("reader", "docling"):          DoclingReaderBuilder(),
    ("reader", "excel"):            ExcelReaderBuilder(),
    ("reader", "field_labeled_csv"): FieldLabeledCsvReaderBuilder(),
    ("reader", "firecrawl"):        FirecrawlReaderBuilder(),
    ("reader", "llms_txt"):         LlmsTxtReaderBuilder(),
    ("reader", "markdown"):         MarkdownReaderBuilder(),
    ("reader", "pptx"):             PptxReaderBuilder(),
    ("reader", "s3"):               S3ReaderBuilder(),
    ("reader", "tavily"):           TavilyReaderBuilder(),
    ("reader", "web_search"):       WebSearchReaderBuilder(),
    ("reader", "wikipedia"):        WikipediaReaderBuilder(),
    # knowledge
    ("knowledge", "base"): KnowledgeBuilder(),
    # db
    ("db", "sqlite"):         SqliteDbBuilder(),
    ("db", "postgres"):       PostgresDbBuilder(),
    ("db", "in_memory"):      InMemoryDbBuilder(),
    ("db", "async_postgres"): AsyncPostgresDbBuilder(),
    ("db", "dynamo"):         DynamoDbBuilder(),
    ("db", "firestore"):      FirestoreDbBuilder(),
    ("db", "gcs_json"):       GcsJsonDbBuilder(),
    ("db", "json"):           JsonDbBuilder(),
    ("db", "mongo"):          MongoDbBuilder(),
    ("db", "mysql"):          MySQLDbBuilder(),
    ("db", "redis"):          RedisDbBuilderDb(),
    ("db", "singlestore"):    SingleStoreDbBuilderDb(),
    ("db", "surrealdb"):      SurrealDbBuilderDb(),
    # agents
    ("agent", "base"):     AgentBuilder(),
    ("agent", "agno_agent"): AgentBuilder(),
    # teams
    ("team", "base"):      TeamBuilder(),
    ("team", "agno_team"): TeamBuilder(),
    # memory
    ("memory", "base"):    MemoryManagerBuilder(),
    # learn
    ("learn", "base"):     LearningMachineBuilder(),
    # compress
    ("compress", "base"):  CompressionManagerBuilder(),
    # guardrails
    ("guardrail", "openai_moderation"):  OpenAIModerationGuardrailBuilder(),
    ("guardrail", "pii_detection"):      PIIDetectionGuardrailBuilder(),
    ("guardrail", "prompt_injection"):   PromptInjectionGuardrailBuilder(),
    # reasoning
    ("reasoning", "base"): ReasoningBuilder(),
    # culture
    ("culture", "base"):          CultureManagerBuilder(),
    # session_summary
    ("session_summary", "base"):  SessionSummaryManagerBuilder(),
    # skills
    ("skill", "base"):            SkillBuilder(),
}

# toolkits：按 catalog 批量注册 + custom 单独注册
for _type_key in TOOLKIT_CATALOG:
    builder_registry[("toolkit", _type_key)] = GenericToolkitBuilder(_type_key)
builder_registry[("toolkit", "custom")] = CustomToolkitBuilder()
