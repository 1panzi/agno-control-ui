import inspect
import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from agno.os.app import AgentOS
from agno.registry import Registry

from core.config import settings
from core.exceptions import AppException
from core.logger import log
from core.response import R


agno_registry = Registry()

# warm_up 及动态注册期间收集的失败记录,供 /api/v1/agno_manage/debug/warmup-errors 查看
warmup_errors: list[dict] = []


def record_warmup_error(row, error: Exception, where: str = "warm_up") -> None:
    """统一记录构建失败信息,带 traceback,便于诊断 team/agent 没法聊天的问题。"""
    tb = traceback.format_exc()
    entry = {
        "where": where,
        "uuid": str(getattr(row, "uuid", "")) or None,
        "name": getattr(row, "name", None),
        "category": getattr(row, "category", None),
        "type": getattr(row, "type", None),
        "error": f"{type(error).__name__}: {error}",
        "traceback": tb,
    }
    warmup_errors.append(entry)
    log.error(
        f"[{where}] build failed uuid={entry['uuid']} "
        f"category={entry['category']} type={entry['type']}: {error}\n{tb}"
    )


async def _warm_up(registry: Registry) -> None:
    """从 ag_resources 加载所有启用的 agent/team 到 agno Registry。"""
    from sqlalchemy import select
    from core.db import SessionLocal, get_agno_db
    from builders.builder_registry import builder_registry
    from core.ref_resolver import RefResolver
    from resources.model import AgResourceModel
    from resources.service import set_agno_registry

    agno_db = get_agno_db()

    set_agno_registry(registry)

    # 每次 warm_up 先清空,避免重复启动时错误累积
    warmup_errors.clear()

    with SessionLocal() as db:
        rows = db.execute(
            select(AgResourceModel).where(
                AgResourceModel.status == "0",
                AgResourceModel.category.in_(["agent", "team"]),
            )
        ).scalars().all()

        agent_count = 0
        team_count = 0

        for row in rows:
            builder = builder_registry.get((row.category, row.type))
            if not builder:
                msg = f"No builder for {row.category}/{row.type}"
                warmup_errors.append({
                    "where": "warm_up",
                    "uuid": str(row.uuid),
                    "name": row.name,
                    "category": row.category,
                    "type": row.type,
                    "error": msg,
                    "traceback": None,
                })
                log.warning(f"[warm_up] {msg} — skip uuid={row.uuid}")
                continue
            try:
                resolver = RefResolver(db=db)
                cfg = {**(row.config or {}), "agent_id": str(row.uuid), "name": row.name}
                obj = builder.build(cfg, resolver)
                if inspect.iscoroutine(obj):
                    obj = await obj
                if not getattr(obj, "db", None):
                    obj.db = agno_db
                if row.category == "agent":
                    registry.agents.append(obj)
                    agent_count += 1
                else:
                    registry.teams.append(obj)
                    team_count += 1
            except Exception as e:
                record_warmup_error(row, e, where="warm_up")

    log.info(
        f"[warm_up] done — agents={agent_count}, teams={team_count}, "
        f"errors={len(warmup_errors)}"
    )


@asynccontextmanager
async def custom_lifespan(app: FastAPI):
    from core.db import Base, engine
    Base.metadata.create_all(engine)
    await _warm_up(agno_registry)
    yield


def _create_base_app() -> FastAPI:
    app = FastAPI(title="agno-platform")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.api_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(AppException)
    async def app_exception_handler(request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content=R.fail(exc.status_code, exc.message).model_dump(),
        )

    from api.v1.router import router
    app.include_router(router)

    return app


_base_app = _create_base_app()

agent_os = AgentOS(
    name="agno-platform",
    db=__import__("core.db", fromlist=["get_agno_db"]).get_agno_db(),
    agents=agno_registry.agents,
    teams=agno_registry.teams,
    registry=agno_registry,
    base_app=_base_app,
    lifespan=custom_lifespan,
    cors_allowed_origins=settings.api_cors_origins,
    on_route_conflict="preserve_base_app",
    telemetry=False,
)

app = agent_os.get_app()


if __name__ == "__main__":
    agent_os.serve(app, host="0.0.0.0", port=8006, reload=True)
