#!/usr/bin/env python
"""测试 Agent 工具调用的脚本。

这个脚本会：
1. 复用已有的 Ollama Provider + ModelConfig（不存在则创建）
2. 查找内置工具（DuckDuckGo、Calculator）
3. 创建一个带工具的 Agent 配置
4. 用会触发工具调用的问题测试对话
"""
import sys

from sqlalchemy.orm import Session
from core.db import SessionLocal, Base, engine
from domains.models.models import Provider, ModelConfig
from domains.tool.models import Tool
from domains.tool.service import seed_builtin_tools
from domains.agent.models import AgentConfig
from domains.agent.schemas import AgentConfigCreate
from domains.agent.service import AgentService


def setup_database():
    print("📦 初始化数据库...")
    Base.metadata.create_all(engine)
    seed_builtin_tools(SessionLocal())
    print("✅ 数据库初始化完成")


def get_or_create_provider(db: Session) -> Provider:
    existing = db.query(Provider).filter(Provider.name == "Ollama-Local").first()
    if existing:
        print(f"✅ 复用 Provider: {existing.name} (ID: {existing.id})")
        return existing

    print("🔧 创建 Ollama Provider...")
    provider = Provider(
        name="Ollama-Local",
        provider_type="ollama",
        api_key="",
        base_url="http://192.168.81.15:7869",
        is_enabled=True,
        is_builtin=False,
        extra_params={},
    )
    db.add(provider)
    db.commit()
    db.refresh(provider)
    print(f"✅ Provider 创建成功: {provider.name} (ID: {provider.id})")
    return provider


def get_or_create_model_config(db: Session, provider: Provider) -> ModelConfig:
    existing = db.query(ModelConfig).filter(ModelConfig.name == "Qwen3.5-9B-Local").first()
    if existing:
        print(f"✅ 复用 ModelConfig: {existing.name} (ID: {existing.id})")
        return existing

    print("🤖 创建 ModelConfig...")
    model_config = ModelConfig(
        name="Qwen3.5-9B-Local",
        provider_id=provider.id,
        model_id="isotnek/qwen3.5:9B-Unsloth-UD-Q4_K_XL",
        temperature=None,
        max_tokens=None,
        is_enabled=True,
        extra_params={},
    )
    db.add(model_config)
    db.commit()
    db.refresh(model_config)
    print(f"✅ ModelConfig 创建成功: {model_config.name} (ID: {model_config.id})")
    return model_config


def get_tools(db: Session, tool_types: list[str]) -> list[Tool]:
    tools = db.query(Tool).filter(Tool.tool_type.in_(tool_types)).all()
    found = {t.tool_type: t for t in tools}
    for t in tool_types:
        if t in found:
            print(f"✅ 找到工具: {found[t].name} (ID: {found[t].id}, type: {t})")
        else:
            print(f"⚠️  工具未找到: {t}（请确认已运行 seed_builtin_tools）")
    return list(found.values())


AGENT_INSTRUCTIONS = [
    "你是一个能够使用工具的智能助手。",
    "当用户问到需要搜索、计算的问题时，优先调用合适的工具。",
    "工具调用完成后，必须用自然语言把结果告诉用户，不能只调用工具不回复。",
    "回答要简洁，并说明使用了哪个工具。",
]


def get_or_create_agent(db: Session, model_config: ModelConfig, tool_ids: list[int]) -> AgentConfig:
    agent_name = "工具测试助手"
    existing = db.query(AgentConfig).filter(AgentConfig.name == agent_name).first()
    if existing:
        existing.tool_ids = tool_ids
        existing.instructions = AGENT_INSTRUCTIONS
        db.commit()
        db.refresh(existing)
        print(f"✅ 复用 Agent: {existing.name} (ID: {existing.id}), tool_ids={existing.tool_ids}")
        return existing

    print("🤖 创建 Agent 配置...")
    agent_service = AgentService(db)
    agent_data = AgentConfigCreate(
        name=agent_name,
        description="用于测试工具调用的助手",
        model_config_id=model_config.id,
        tool_ids=tool_ids,
        instructions=AGENT_INSTRUCTIONS,
        settings={"markdown": True},
    )
    agent = agent_service.create(agent_data)
    print(f"✅ Agent 创建成功: {agent.name} (ID: {agent.id})")
    return agent


async def run_conversation(db: Session, agent: AgentConfig):
    print("\n💬 开始工具调用测试...")
    print("=" * 60)

    svc = AgentService(db)
    session_id = None

    questions = [
        ("Calculator", "请用计算工具算 123 乘以 456 等于多少？"),
        ("Wikipedia",  "请用 Wikipedia 工具搜索 'Python programming language'，然后用中文总结主要内容。"),
        ("多轮上下文",  "不要再搜索了，根据你刚才查到的 Wikipedia 内容，直接回答：Python 最初是哪一年发布的？"),
    ]

    for label, message in questions:
        print(f"\n🔍 [{label}]")
        print(f"👤 用户: {message}")
        print("🤖 助手: ", end="", flush=True)
        try:
            reply, session_id = await svc.chat(agent.id, message, session_id)
            print(reply)
            print(f"   (session_id: {session_id})")
        except Exception as e:
            print(f"\n❌ 失败: {e}")
            import traceback
            traceback.print_exc()
            raise

    print("\n" + "=" * 60)
    print("✅ 工具调用测试完成！")


async def main():
    print("🚀 开始测试 Agent 工具调用")
    print("=" * 60)

    setup_database()
    db = SessionLocal()

    try:
        provider = get_or_create_provider(db)
        model_config = get_or_create_model_config(db, provider)

        print("\n🔧 查找内置工具...")
        tools = get_tools(db, ["wikipedia", "calculator"])
        if not tools:
            print("❌ 没有找到任何工具，请先启动服务让 seed_builtin_tools 运行")
            sys.exit(1)

        tool_ids = [t.id for t in tools]
        agent = get_or_create_agent(db, model_config, tool_ids)

        await run_conversation(db, agent)

        print("\n🎉 所有测试完成！")

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
