"""
Knowledge、Memory、Compress、Culture、SessionSummary、Learn、Reasoning builders build() 测试。
"""
import pytest
from unittest.mock import MagicMock, AsyncMock


@pytest.fixture
def resolver():
    m = MagicMock()
    m.resolve = AsyncMock(return_value=None)
    m.resolve_list = AsyncMock(return_value=[])
    return m


@pytest.fixture
def mock_model():
    from agno.models.openai import OpenAIChat
    return OpenAIChat(id="gpt-4o", api_key="sk-test")


# ── Knowledge ────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_knowledge_build(resolver):
    from builders.knowledge.base import KnowledgeBuilder
    mock_vectordb = MagicMock()
    resolver.resolve = AsyncMock(return_value=mock_vectordb)
    obj = await KnowledgeBuilder().build({"vectordb": {"ref": "fake-uuid"}, "max_results": 5}, resolver)
    from agno.knowledge import Knowledge
    assert isinstance(obj, Knowledge)


@pytest.mark.asyncio
async def test_knowledge_build_no_vectordb(resolver):
    from builders.knowledge.base import KnowledgeBuilder
    resolver.resolve = AsyncMock(return_value=None)
    obj = await KnowledgeBuilder().build({}, resolver)
    from agno.knowledge import Knowledge
    assert isinstance(obj, Knowledge)


def test_knowledge_category_type():
    from builders.knowledge.base import KnowledgeBuilder
    assert KnowledgeBuilder.category == "knowledge"
    assert KnowledgeBuilder.type == "base"


# ── Memory ────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_memory_build_no_model(resolver):
    from builders.memory.base import MemoryManagerBuilder
    obj = await MemoryManagerBuilder().build({}, resolver)
    from agno.memory.manager import MemoryManager
    assert isinstance(obj, MemoryManager)


@pytest.mark.asyncio
async def test_memory_build_with_model(resolver, mock_model):
    from builders.memory.base import MemoryManagerBuilder
    resolver.resolve = AsyncMock(return_value=mock_model)
    obj = await MemoryManagerBuilder().build({"model": {"ref": "uuid"}}, resolver)
    from agno.memory.manager import MemoryManager
    assert isinstance(obj, MemoryManager)
    assert obj.model is mock_model


@pytest.mark.asyncio
async def test_memory_build_flags(resolver):
    from builders.memory.base import MemoryManagerBuilder
    obj = await MemoryManagerBuilder().build({"delete_memories": True, "clear_memories": True}, resolver)
    assert obj.delete_memories is True
    assert obj.clear_memories is True


def test_memory_category_type():
    from builders.memory.base import MemoryManagerBuilder
    assert MemoryManagerBuilder.category == "memory"
    assert MemoryManagerBuilder.type == "base"


# ── Compress ──────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_compress_build(resolver):
    from builders.compress.base import CompressionManagerBuilder
    obj = await CompressionManagerBuilder().build({}, resolver)
    from agno.compression.manager import CompressionManager
    assert isinstance(obj, CompressionManager)


@pytest.mark.asyncio
async def test_compress_build_with_model(resolver, mock_model):
    from builders.compress.base import CompressionManagerBuilder
    resolver.resolve = AsyncMock(return_value=mock_model)
    obj = await CompressionManagerBuilder().build({"model": {"ref": "uuid"}}, resolver)
    assert obj.model is mock_model


def test_compress_category_type():
    from builders.compress.base import CompressionManagerBuilder
    assert CompressionManagerBuilder.category == "compress"
    assert CompressionManagerBuilder.type == "base"


# ── Culture ───────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_culture_build(resolver):
    from builders.culture.base import CultureManagerBuilder
    obj = await CultureManagerBuilder().build({}, resolver)
    from agno.culture.manager import CultureManager
    assert isinstance(obj, CultureManager)


@pytest.mark.asyncio
async def test_culture_build_flags(resolver):
    from builders.culture.base import CultureManagerBuilder
    obj = await CultureManagerBuilder().build({"delete_knowledge": True}, resolver)
    assert obj.delete_knowledge is True


def test_culture_category_type():
    from builders.culture.base import CultureManagerBuilder
    assert CultureManagerBuilder.category == "culture"
    assert CultureManagerBuilder.type == "base"


# ── SessionSummary ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_session_summary_build(resolver):
    from builders.session_summary.base import SessionSummaryManagerBuilder
    obj = await SessionSummaryManagerBuilder().build({}, resolver)
    from agno.session.summary import SessionSummaryManager
    assert isinstance(obj, SessionSummaryManager)


@pytest.mark.asyncio
async def test_session_summary_build_with_model(resolver, mock_model):
    from builders.session_summary.base import SessionSummaryManagerBuilder
    resolver.resolve = AsyncMock(return_value=mock_model)
    obj = await SessionSummaryManagerBuilder().build({"model": {"ref": "uuid"}}, resolver)
    assert obj.model is mock_model


def test_session_summary_category_type():
    from builders.session_summary.base import SessionSummaryManagerBuilder
    assert SessionSummaryManagerBuilder.category == "session_summary"
    assert SessionSummaryManagerBuilder.type == "base"


# ── Learn ─────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_learn_build(resolver):
    from builders.learn.base import LearningMachineBuilder
    obj = await LearningMachineBuilder().build({}, resolver)
    from agno.learn.machine import LearningMachine
    assert isinstance(obj, LearningMachine)


@pytest.mark.asyncio
async def test_learn_build_with_flags(resolver):
    from builders.learn.base import LearningMachineBuilder
    obj = await LearningMachineBuilder().build({
        "enable_user_profile": True,
        "enable_user_memory": True,
        "namespace": "test-ns",
    }, resolver)
    assert obj.user_profile is True
    assert obj.namespace == "test-ns"


def test_learn_category_type():
    from builders.learn.base import LearningMachineBuilder
    assert LearningMachineBuilder.category == "learn"
    assert LearningMachineBuilder.type == "base"


# ── Reasoning ─────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_reasoning_build_returns_dict(resolver):
    from builders.reasoning.base import ReasoningBuilder
    result = await ReasoningBuilder().build({}, resolver)
    assert isinstance(result, dict)
    assert "min_steps" in result
    assert "max_steps" in result


@pytest.mark.asyncio
async def test_reasoning_build_custom_steps(resolver):
    from builders.reasoning.base import ReasoningBuilder
    result = await ReasoningBuilder().build({"min_steps": 2, "max_steps": 5}, resolver)
    assert result["min_steps"] == 2
    assert result["max_steps"] == 5


@pytest.mark.asyncio
async def test_reasoning_build_with_model(resolver, mock_model):
    from builders.reasoning.base import ReasoningBuilder
    resolver.resolve = AsyncMock(return_value=mock_model)
    result = await ReasoningBuilder().build({"model": {"ref": "uuid"}}, resolver)
    assert result["reasoning_model"] is mock_model


def test_reasoning_category_type():
    from builders.reasoning.base import ReasoningBuilder
    assert ReasoningBuilder.category == "reasoning"
    assert ReasoningBuilder.type == "base"
