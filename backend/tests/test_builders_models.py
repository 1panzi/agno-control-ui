"""
Model builders build() 测试。
provider 包未安装时自动跳过对应测试。
"""
import pytest
from unittest.mock import MagicMock

from builders.models.openai import OpenAIModelBuilder
from builders.models.anthropic import AnthropicModelBuilder
from builders.models.ollama import OllamaModelBuilder
from builders.models.groq import GroqModelBuilder
from builders.models.deepseek import DeepSeekModelBuilder
from builders.models.mistral import MistralModelBuilder
from builders.models.azure import AzureModelBuilder
from builders.models.cohere import CohereModelBuilder
from builders.models.together import TogetherModelBuilder
from builders.models.openai_like import OpenAILikeModelBuilder


@pytest.fixture
def resolver():
    return MagicMock()


def test_openai_build(resolver):
    obj = OpenAIModelBuilder().build({"model_id": "gpt-4o", "api_key": "sk-test"}, resolver)
    from agno.models.openai import OpenAIChat
    assert isinstance(obj, OpenAIChat)
    assert obj.id == "gpt-4o"


def test_openai_build_with_temperature(resolver):
    obj = OpenAIModelBuilder().build({"model_id": "gpt-4o", "temperature": 0.5, "max_tokens": 1000}, resolver)
    assert obj.temperature == 0.5
    assert obj.max_tokens == 1000


def test_openai_schema_has_fields():
    names = [f["name"] for f in OpenAIModelBuilder().schema]
    assert "model_id" in names
    assert "api_key" in names
    assert "temperature" in names


def test_anthropic_build(resolver):
    pytest.importorskip("anthropic")
    obj = AnthropicModelBuilder().build({"model_id": "claude-3-5-sonnet-20241022", "api_key": "sk-ant"}, resolver)
    from agno.models.anthropic import Claude
    assert isinstance(obj, Claude)
    assert obj.id == "claude-3-5-sonnet-20241022"


def test_ollama_build(resolver):
    obj = OllamaModelBuilder().build({"model_id": "llama3.2"}, resolver)
    from agno.models.ollama import Ollama
    assert isinstance(obj, Ollama)
    assert obj.id == "llama3.2"


def test_ollama_build_with_host(resolver):
    obj = OllamaModelBuilder().build({"model_id": "llama3.2", "base_url": "http://localhost:11434"}, resolver)
    assert obj.host == "http://localhost:11434"


def test_groq_build(resolver):
    pytest.importorskip("groq")
    obj = GroqModelBuilder().build({"model_id": "llama-3.1-70b-versatile", "api_key": "gsk-test"}, resolver)
    from agno.models.groq import Groq
    assert isinstance(obj, Groq)
    assert obj.id == "llama-3.1-70b-versatile"


def test_deepseek_build(resolver):
    obj = DeepSeekModelBuilder().build({"model_id": "deepseek-chat", "api_key": "sk-ds"}, resolver)
    from agno.models.deepseek import DeepSeek
    assert isinstance(obj, DeepSeek)
    assert obj.id == "deepseek-chat"


def test_mistral_build(resolver):
    pytest.importorskip("mistralai")
    obj = MistralModelBuilder().build({"model_id": "mistral-large-latest", "api_key": "sk-ms"}, resolver)
    from agno.models.mistral import MistralChat
    assert isinstance(obj, MistralChat)
    assert obj.id == "mistral-large-latest"


def test_azure_build(resolver):
    obj = AzureModelBuilder().build({
        "model_id": "gpt-4o",
        "base_url": "https://my.openai.azure.com",
        "api_key": "sk-az",
        "azure_deployment": "my-deployment",
    }, resolver)
    from agno.models.azure import AzureOpenAI
    assert isinstance(obj, AzureOpenAI)
    assert obj.id == "gpt-4o"


def test_cohere_build(resolver):
    pytest.importorskip("cohere")
    obj = CohereModelBuilder().build({"model_id": "command-r-plus", "api_key": "co-test"}, resolver)
    from agno.models.cohere import CohereChat
    assert isinstance(obj, CohereChat)
    assert obj.id == "command-r-plus"


def test_together_build(resolver):
    obj = TogetherModelBuilder().build({"model_id": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", "api_key": "tog-test"}, resolver)
    from agno.models.together import Together
    assert isinstance(obj, Together)


def test_openai_like_build(resolver):
    obj = OpenAILikeModelBuilder().build({
        "model_id": "custom-model",
        "base_url": "http://localhost:8080/v1",
        "api_key": "sk-custom",
    }, resolver)
    from agno.models.openai.like import OpenAILike
    assert isinstance(obj, OpenAILike)
    assert obj.base_url == "http://localhost:8080/v1"


def test_builder_category_and_type():
    assert OpenAIModelBuilder.category == "model"
    assert OpenAIModelBuilder.type == "openai"
    assert AnthropicModelBuilder.type == "anthropic"
    assert OllamaModelBuilder.type == "ollama"
    assert GroqModelBuilder.type == "groq"
    assert DeepSeekModelBuilder.type == "deepseek"
    assert MistralModelBuilder.type == "mistral"
    assert AzureModelBuilder.type == "azure"
    assert CohereModelBuilder.type == "cohere"
    assert TogetherModelBuilder.type == "together"
    assert OpenAILikeModelBuilder.type == "openai_like"
