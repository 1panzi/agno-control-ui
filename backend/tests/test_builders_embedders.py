"""
Embedder builders build() 测试。
provider 包未安装时自动跳过。
"""
import pytest
from unittest.mock import MagicMock

from builders.embedders.openai import OpenAIEmbedderBuilder
from builders.embedders.azure import AzureEmbedderBuilder
from builders.embedders.ollama import OllamaEmbedderBuilder
from builders.embedders.cohere import CohereEmbedderBuilder
from builders.embedders.google import GoogleEmbedderBuilder


@pytest.fixture
def resolver():
    return MagicMock()


def test_openai_embedder_build(resolver):
    obj = OpenAIEmbedderBuilder().build({"model_id": "text-embedding-3-small", "api_key": "sk-test"}, resolver)
    from agno.knowledge.embedder.openai import OpenAIEmbedder
    assert isinstance(obj, OpenAIEmbedder)
    assert obj.id == "text-embedding-3-small"


def test_openai_embedder_with_dimensions(resolver):
    obj = OpenAIEmbedderBuilder().build({"model_id": "text-embedding-3-large", "dimensions": 512}, resolver)
    assert obj.dimensions == 512


def test_azure_embedder_build(resolver):
    obj = AzureEmbedderBuilder().build({
        "model_id": "text-embedding-ada-002",
        "base_url": "https://my.openai.azure.com",
        "api_key": "sk-az",
    }, resolver)
    from agno.knowledge.embedder.azure_openai import AzureOpenAIEmbedder
    assert isinstance(obj, AzureOpenAIEmbedder)


def test_ollama_embedder_build(resolver):
    obj = OllamaEmbedderBuilder().build({"model_id": "nomic-embed-text"}, resolver)
    from agno.knowledge.embedder.ollama import OllamaEmbedder
    assert isinstance(obj, OllamaEmbedder)
    assert obj.id == "nomic-embed-text"


def test_cohere_embedder_build(resolver):
    pytest.importorskip("cohere")
    obj = CohereEmbedderBuilder().build({"model_id": "embed-english-v3.0", "api_key": "co-test"}, resolver)
    from agno.knowledge.embedder.cohere import CohereEmbedder
    assert isinstance(obj, CohereEmbedder)


def test_google_embedder_build(resolver):
    pytest.importorskip("google.generativeai", reason="google-genai not installed")
    obj = GoogleEmbedderBuilder().build({"model_id": "text-embedding-004", "api_key": "goog-test"}, resolver)
    from agno.knowledge.embedder.google import GeminiEmbedder
    assert isinstance(obj, GeminiEmbedder)


def test_embedder_schema_has_model_id():
    for builder in [OpenAIEmbedderBuilder(), OllamaEmbedderBuilder()]:
        names = [f["name"] for f in builder.schema]
        assert "model_id" in names, f"{builder.__class__.__name__} schema missing 'model_id'"


def test_embedder_category_and_type():
    assert OpenAIEmbedderBuilder.category == "embedder"
    assert OpenAIEmbedderBuilder.type == "openai"
    assert AzureEmbedderBuilder.type == "azure"
    assert OllamaEmbedderBuilder.type == "ollama"
    assert CohereEmbedderBuilder.type == "cohere"
    assert GoogleEmbedderBuilder.type == "google"
