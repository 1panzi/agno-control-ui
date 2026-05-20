"""
Agent 和 Team builders build() 测试。
"""
import pytest
from unittest.mock import MagicMock, AsyncMock


@pytest.fixture
def mock_model():
    from agno.models.openai import OpenAIChat
    return OpenAIChat(id="gpt-4o", api_key="sk-test")


@pytest.fixture
def resolver(mock_model):
    m = MagicMock()

    async def _resolve(v):
        if v is None:
            return None
        if isinstance(v, dict) and v.get("ref"):
            return mock_model
        return None

    m.resolve = AsyncMock(side_effect=_resolve)
    m.resolve_list = AsyncMock(return_value=[])
    return m


@pytest.fixture
def resolver_none():
    m = MagicMock()
    m.resolve = AsyncMock(return_value=None)
    m.resolve_list = AsyncMock(return_value=[])
    return m


# ── AgentBuilder ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_agent_build_minimal(resolver, mock_model):
    from builders.agents.base import AgentBuilder

    builder = AgentBuilder()
    obj = await builder.build(
        {"model": {"ref": "fake-uuid"}},
        resolver,
    )
    from agno.agent import Agent
    assert isinstance(obj, Agent)
    assert obj.model is mock_model


@pytest.mark.asyncio
async def test_agent_build_with_name_and_instructions(resolver):
    from builders.agents.base import AgentBuilder

    builder = AgentBuilder()
    obj = await builder.build(
        {
            "model": {"ref": "fake-uuid"},
            "name": "my-agent",
            "instructions": "你是一个助手",
        },
        resolver,
    )
    assert obj.name == "my-agent"
    assert obj.instructions == "你是一个助手"


@pytest.mark.asyncio
async def test_agent_build_markdown_default_true(resolver):
    from builders.agents.base import AgentBuilder

    builder = AgentBuilder()
    obj = await builder.build({"model": {"ref": "uuid"}}, resolver)
    assert obj.markdown is True


@pytest.mark.asyncio
async def test_agent_build_markdown_false(resolver):
    from builders.agents.base import AgentBuilder

    builder = AgentBuilder()
    obj = await builder.build({"model": {"ref": "uuid"}, "markdown": False}, resolver)
    assert obj.markdown is False


@pytest.mark.asyncio
async def test_agent_build_with_agent_id(resolver):
    from builders.agents.base import AgentBuilder

    builder = AgentBuilder()
    obj = await builder.build(
        {"model": {"ref": "uuid"}, "agent_id": "custom-id-123"},
        resolver,
    )
    assert obj.id == "custom-id-123"


@pytest.mark.asyncio
async def test_agent_build_with_tools(resolver, mock_model):
    from builders.agents.base import AgentBuilder

    mock_tool = MagicMock()
    resolver.resolve_list = AsyncMock(return_value=[mock_tool])
    builder = AgentBuilder()
    obj = await builder.build(
        {"model": {"ref": "uuid"}, "tools": [{"ref": "tool-uuid"}]},
        resolver,
    )
    assert obj.tools is not None
    assert mock_tool in obj.tools


@pytest.mark.asyncio
async def test_agent_build_with_memory_manager(resolver, mock_model):
    from builders.agents.base import AgentBuilder
    from agno.memory.manager import MemoryManager

    mock_memory = MemoryManager()
    call_count = {"n": 0}

    async def _resolve(v):
        if v is None:
            return None
        call_count["n"] += 1
        return mock_model if call_count["n"] == 1 else mock_memory

    resolver.resolve = AsyncMock(side_effect=_resolve)
    builder = AgentBuilder()
    obj = await builder.build(
        {"model": {"ref": "uuid"}, "memory_manager": {"ref": "mem-uuid"}},
        resolver,
    )
    assert obj.memory_manager is not None


@pytest.mark.asyncio
async def test_agent_build_with_reasoning(resolver, mock_model):
    from builders.agents.base import AgentBuilder

    reasoning_dict = {"reasoning_model": mock_model, "min_steps": 2, "max_steps": 8}
    resolve_calls = {"count": 0}

    async def side_effect(v):
        if v is None:
            return None
        resolve_calls["count"] += 1
        if resolve_calls["count"] == 1:
            return mock_model
        return reasoning_dict

    resolver.resolve = AsyncMock(side_effect=side_effect)
    builder = AgentBuilder()
    obj = await builder.build(
        {"model": {"ref": "uuid"}, "reasoning_config": {"ref": "r-uuid"}},
        resolver,
    )
    assert obj.reasoning is True
    assert obj.reasoning_min_steps == 2
    assert obj.reasoning_max_steps == 8


@pytest.mark.asyncio
async def test_agent_build_enable_agentic_memory(resolver):
    from builders.agents.base import AgentBuilder

    builder = AgentBuilder()
    obj = await builder.build(
        {"model": {"ref": "uuid"}, "enable_agentic_memory": True},
        resolver,
    )
    assert obj.enable_agentic_memory is True


def test_agent_builder_schema_has_required_fields():
    from builders.agents.base import AgentBuilder

    builder = AgentBuilder()
    names = [f["name"] for f in builder.schema]
    for field in ["model", "tools", "knowledge", "name", "instructions", "markdown"]:
        assert field in names, f"AgentBuilder schema missing field: {field}"


def test_agent_category_type():
    from builders.agents.base import AgentBuilder
    assert AgentBuilder.category == "agent"
    assert AgentBuilder.type == "base"


# ── TeamBuilder ───────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_team_build_minimal(resolver, mock_model):
    from builders.teams.base import TeamBuilder
    from agno.agent import Agent

    mock_member = Agent(model=mock_model, id="member-1")
    resolver.resolve = AsyncMock(return_value=mock_model)
    resolver.resolve_list = AsyncMock(return_value=[mock_member])

    builder = TeamBuilder()
    obj = await builder.build(
        {
            "model": {"ref": "uuid"},
            "members": [{"ref": "agent-uuid"}],
        },
        resolver,
    )
    from agno.team import Team
    assert isinstance(obj, Team)


@pytest.mark.asyncio
async def test_team_build_with_name(resolver, mock_model):
    from builders.teams.base import TeamBuilder
    from agno.agent import Agent

    mock_member = Agent(model=mock_model, id="member-1")
    resolver.resolve = AsyncMock(return_value=mock_model)
    resolver.resolve_list = AsyncMock(return_value=[mock_member])

    builder = TeamBuilder()
    obj = await builder.build(
        {
            "model": {"ref": "uuid"},
            "members": [{"ref": "agent-uuid"}],
            "name": "my-team",
            "mode": "coordinate",
        },
        resolver,
    )
    assert obj.name == "my-team"


@pytest.mark.asyncio
async def test_team_build_markdown_default(resolver, mock_model):
    from builders.teams.base import TeamBuilder
    from agno.agent import Agent

    mock_member = Agent(model=mock_model, id="m1")
    resolver.resolve = AsyncMock(return_value=mock_model)
    resolver.resolve_list = AsyncMock(return_value=[mock_member])

    builder = TeamBuilder()
    obj = await builder.build(
        {"model": {"ref": "uuid"}, "members": [{"ref": "uuid"}]},
        resolver,
    )
    assert obj.markdown is True


def test_team_builder_schema_has_fields():
    from builders.teams.base import TeamBuilder

    builder = TeamBuilder()
    names = [f["name"] for f in builder.schema]
    assert "model" in names
    assert "members" in names
    assert "mode" in names


def test_team_category_type():
    from builders.teams.base import TeamBuilder
    assert TeamBuilder.category == "team"
    assert TeamBuilder.type == "base"
