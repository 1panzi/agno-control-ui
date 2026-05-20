#!/usr/bin/env python
"""测试 Agent Chat 接口的脚本。

这个脚本会：
1. 创建一个 Ollama Provider
2. 创建一个 ModelConfig
3. 创建一个 Agent 配置
4. 调用 chat 接口测试对话
"""
import sys

from sqlalchemy.orm import Session
from core.db import SessionLocal, Base, engine
from domains.models.models import Provider, ModelConfig
from domains.models.schemas import ProviderIn, ModelConfigIn
from domains.agent.models import AgentConfig
from domains.agent.schemas import AgentConfigCreate
from domains.agent.service import AgentService


def setup_database():
    """初始化数据库表。"""
    print("📦 初始化数据库...")
    Base.metadata.create_all(engine)
    print("✅ 数据库初始化完成")


def create_ollama_provider(db: Session) -> Provider:
    """创建 Ollama Provider。"""
    print("\n🔧 创建 Ollama Provider...")

    # 检查是否已存在
    existing = db.query(Provider).filter(Provider.name == "Ollama-Local").first()
    if existing:
        print(f"✅ Provider 已存在: {existing.name} (ID: {existing.id})")
        return existing

    provider = Provider(
        name="Ollama-Local",
        provider_type="ollama",
        api_key="",  # Ollama 不需要 API key
        base_url="http://192.168.81.15:7869",
        is_enabled=True,
        is_builtin=False,
        extra_params={}
    )
    db.add(provider)
    db.commit()
    db.refresh(provider)
    print(f"✅ Provider 创建成功: {provider.name} (ID: {provider.id})")
    return provider


def create_model_config(db: Session, provider: Provider) -> ModelConfig:
    """创建 ModelConfig。"""
    print("\n🤖 创建 ModelConfig...")

    # 检查是否已存在
    existing = db.query(ModelConfig).filter(
        ModelConfig.name == "Qwen3.5-9B-Local"
    ).first()
    if existing:
        print(f"✅ ModelConfig 已存在: {existing.name} (ID: {existing.id})")
        return existing

    model_config = ModelConfig(
        name="Qwen3.5-9B-Local",
        provider_id=provider.id,
        model_id="isotnek/qwen3.5:9B-Unsloth-UD-Q4_K_XL",
        temperature=None,  # Ollama 不支持 temperature 参数
        max_tokens=None,   # Ollama 不支持 max_tokens 参数
        is_enabled=True,
        extra_params={}
    )
    db.add(model_config)
    db.commit()
    db.refresh(model_config)
    print(f"✅ ModelConfig 创建成功: {model_config.name} (ID: {model_config.id})")
    return model_config


def create_agent_config(db: Session, model_config: ModelConfig) -> AgentConfig:
    """创建 Agent 配置。"""
    print("\n🤖 创建 Agent 配置...")

    # 检查是否已存在
    existing = db.query(AgentConfig).filter(
        AgentConfig.name == "测试助手"
    ).first()
    if existing:
        print(f"✅ Agent 配置已存在: {existing.name} (ID: {existing.id})")
        return existing

    agent_service = AgentService(db)
    agent_data = AgentConfigCreate(
        name="测试助手",
        description="用于测试的简单对话助手",
        model_config_id=model_config.id,
        instructions=[
            "你是一个友好的助手。",
            "请用简洁明了的语言回答问题。",
            "如果不确定答案，请诚实地说不知道。"
        ],
        settings={
            "markdown": True,
            "temperature": 0.7
        }
    )
    agent = agent_service.create(agent_data)
    print(f"✅ Agent 配置创建成功: {agent.name} (ID: {agent.id})")
    return agent


async def test_chat(db: Session, agent: AgentConfig):
    """测试 chat 接口。"""
    print("\n💬 开始测试对话...")
    print("=" * 60)

    agent_service = AgentService(db)

    # 测试对话 1
    message1 = "你好！你是什么模型？是chatgpt吗 还是千问"
    print(f"\n👤 用户: {message1}")
    print("🤖 助手: ", end="", flush=True)

    try:
        reply1, session_id = await agent_service.chat(agent.id, message1)
        print(reply1)
        print(f"\n📝 Session ID: {session_id}")

        # 测试对话 2（使用相同的 session_id）
        message2 = "1+10等于几？"
        print(f"\n👤 用户: {message2}")
        print("🤖 助手: ", end="", flush=True)

        reply2, session_id2 = await agent_service.chat(agent.id, message2, session_id)
        print(reply2)
        print(f"\n📝 Session ID: {session_id2}")

        print("\n" + "=" * 60)
        print("✅ 对话测试成功！")

    except Exception as e:
        print(f"\n❌ 对话测试失败: {e}")
        import traceback
        traceback.print_exc()
        raise


async def main():
    """主函数。"""
    print("🚀 开始测试 Agent Chat 接口")
    print("=" * 60)

    # 初始化数据库
    setup_database()

    # 创建数据库会话
    db = SessionLocal()

    try:
        # 1. 创建 Provider
        provider = create_ollama_provider(db)

        # 2. 创建 ModelConfig
        model_config = create_model_config(db, provider)

        # 3. 创建 Agent 配置
        agent = create_agent_config(db, model_config)

        # 4. 测试对话
        await test_chat(db, agent)

        print("\n" + "=" * 60)
        print("🎉 所有测试完成！")

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
