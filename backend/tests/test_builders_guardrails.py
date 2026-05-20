"""
Guardrail builders build() 测试。
"""
import pytest
from unittest.mock import MagicMock

from builders.guardrails.base import (
    OpenAIModerationGuardrailBuilder,
    PIIDetectionGuardrailBuilder,
    PromptInjectionGuardrailBuilder,
)


@pytest.fixture
def resolver():
    return MagicMock()


@pytest.mark.asyncio
async def test_openai_moderation_build(resolver):
    builder = OpenAIModerationGuardrailBuilder()
    obj = await builder.build({"api_key": "sk-test"}, resolver)
    from agno.guardrails.openai import OpenAIModerationGuardrail
    assert isinstance(obj, OpenAIModerationGuardrail)


@pytest.mark.asyncio
async def test_openai_moderation_default_model(resolver):
    builder = OpenAIModerationGuardrailBuilder()
    obj = await builder.build({}, resolver)
    assert obj.moderation_model == "omni-moderation-latest"


@pytest.mark.asyncio
async def test_pii_detection_build(resolver):
    builder = PIIDetectionGuardrailBuilder()
    obj = await builder.build({}, resolver)
    from agno.guardrails.pii import PIIDetectionGuardrail
    assert isinstance(obj, PIIDetectionGuardrail)


@pytest.mark.asyncio
async def test_prompt_injection_build(resolver):
    builder = PromptInjectionGuardrailBuilder()
    obj = await builder.build({}, resolver)
    from agno.guardrails.prompt_injection import PromptInjectionGuardrail
    assert isinstance(obj, PromptInjectionGuardrail)


@pytest.mark.asyncio
async def test_prompt_injection_with_patterns(resolver):
    builder = PromptInjectionGuardrailBuilder()
    obj = await builder.build({"injection_patterns": "ignore previous\ndisregard"}, resolver)
    from agno.guardrails.prompt_injection import PromptInjectionGuardrail
    assert isinstance(obj, PromptInjectionGuardrail)
    assert len(obj.injection_patterns) == 2


def test_guardrail_category_and_types():
    assert OpenAIModerationGuardrailBuilder.category == "guardrail"
    assert OpenAIModerationGuardrailBuilder.type == "openai_moderation"
    assert PIIDetectionGuardrailBuilder.category == "guardrail"
    assert PIIDetectionGuardrailBuilder.type == "pii_detection"
    assert PromptInjectionGuardrailBuilder.category == "guardrail"
    assert PromptInjectionGuardrailBuilder.type == "prompt_injection"
