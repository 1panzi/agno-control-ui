"""
诊断端点 —— 用于排查 agent/team 是否成功注册到 AgentOS。

与 agno 原生 /agents、/teams 接口对比:
- agno 原生 /agents、/teams 列表接口可能走 Registry / DB 合并逻辑,
  不总能反映 warm_up 实际构建成功的对象;
- 这里直接读 `agno_registry` 内存列表 + warm_up 期间收集的失败记录,
  方便用户一眼看清「为什么 team 聊天没响应」。
"""

from fastapi import APIRouter

from core.response import R


DebugRouter = APIRouter(prefix="/v1/agno_manage/debug", tags=["诊断"])


def _dump_entity(obj) -> dict:
    return {
        "id": getattr(obj, "id", None),
        "name": getattr(obj, "name", None),
        "class": type(obj).__name__,
        "has_db": getattr(obj, "db", None) is not None,
    }


@DebugRouter.get("/registry", summary="查看 agno Registry 注册状态")
async def get_registry_state():
    from main import agno_registry, warmup_errors

    return R.ok(data={
        "agents": [_dump_entity(a) for a in agno_registry.agents],
        "teams": [_dump_entity(t) for t in agno_registry.teams],
        "agent_count": len(agno_registry.agents),
        "team_count": len(agno_registry.teams),
        "warmup_errors": warmup_errors,
    })


@DebugRouter.get("/warmup-errors", summary="查看 warm_up / 动态注册失败记录")
async def get_warmup_errors():
    from main import warmup_errors

    return R.ok(data=warmup_errors)
