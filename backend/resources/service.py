import inspect

from sqlalchemy.orm import Session

from builders.builder_registry import builder_registry
from core.exceptions import CustomException
from core.logger import log
from core.ref_resolver import RefResolver
from resources.crud import AgResourceCRUD
from resources.model import AgResourceModel
from resources.schema import (
    AgResourceCreateSchema,
    AgResourceOutSchema,
    AgResourceUpdateSchema,
)

_agno_registry = None


def set_agno_registry(registry) -> None:
    global _agno_registry
    _agno_registry = registry


def get_agno_registry():
    assert _agno_registry is not None, "agno Registry not initialized"
    return _agno_registry


async def _build_and_register(row: AgResourceModel, db: Session) -> None:
    """根据 row 构建 agno 对象，注册到 agno Registry（仅 agent/team）。"""
    from core.db import get_agno_db
    builder = builder_registry.get((row.category, row.type))
    if not builder:
        return
    resolver = RefResolver(db=db)
    cfg = {**(row.config or {}), "agent_id": str(row.uuid), "name": row.name}
    obj = builder.build(cfg, resolver)
    if inspect.iscoroutine(obj):
        obj = await obj
    if not getattr(obj, "db", None):
        obj.db = get_agno_db()
    registry = get_agno_registry()
    uuid = str(row.uuid)
    if row.category == "agent":
        registry.agents[:] = [a for a in registry.agents if getattr(a, "id", None) != uuid]
        registry.agents.append(obj)
    elif row.category == "team":
        registry.teams[:] = [t for t in registry.teams if getattr(t, "id", None) != uuid]
        registry.teams.append(obj)


def _remove_from_registry(uuid: str, category: str) -> None:
    """从 agno Registry 中移除 agent/team。"""
    registry = get_agno_registry()
    if category == "agent":
        registry.agents[:] = [a for a in registry.agents if getattr(a, "id", None) != uuid]
    elif category == "team":
        registry.teams[:] = [t for t in registry.teams if getattr(t, "id", None) != uuid]


def _record_register_error(row: AgResourceModel, error: Exception, where: str) -> None:
    """动态注册失败时,复用 main.record_warmup_error 统一记录带 traceback 的错误。"""
    # lazy import 规避 service ↔ main 循环依赖
    from main import record_warmup_error
    record_warmup_error(row, error, where=where)


class AgResourceService:

    @classmethod
    async def detail(cls, db: Session, id: int) -> dict:
        row = AgResourceCRUD(db).get_by_id(id)
        if not row:
            raise CustomException(msg="该数据不存在", status_code=404)
        result = AgResourceOutSchema.model_validate(row).model_dump(mode="json")
        builder = builder_registry.get((row.category, row.type))
        if builder:
            full_config = {}
            for field in builder.schema:
                name = field["name"]
                if name in (row.config or {}):
                    full_config[name] = row.config[name]
                elif "default" in field:
                    full_config[name] = field["default"]
            result["config"] = full_config
        return result

    @classmethod
    async def page(cls, db: Session, query) -> dict:
        result = AgResourceCRUD(db).page(
            page=query.page,
            page_size=query.page_size,
            name=query.name,
            category=query.category,
            type=query.type,
            status=query.status,
        )
        result["items"] = [
            AgResourceOutSchema.model_validate(r).model_dump(mode="json") for r in result["items"]
        ]
        return result

    @classmethod
    async def create(cls, db: Session, data: AgResourceCreateSchema) -> dict:
        row = AgResourceCRUD(db).create(data)
        db.commit()
        db.refresh(row)
        if row.status == "0" and row.category in ("agent", "team"):
            try:
                await _build_and_register(row, db)
            except Exception as e:
                _record_register_error(row, e, "create")
        return AgResourceOutSchema.model_validate(row).model_dump(mode="json")

    @classmethod
    async def update(cls, db: Session, id: int, data: AgResourceUpdateSchema) -> dict:
        crud = AgResourceCRUD(db)
        if not crud.get_by_id(id):
            raise CustomException(msg="更新失败，该数据不存在", status_code=404)
        row = crud.update(id, data)
        db.commit()
        db.refresh(row)
        if row.category in ("agent", "team"):
            uuid = str(row.uuid)
            try:
                if row.status == "0":
                    await _build_and_register(row, db)
                else:
                    _remove_from_registry(uuid, row.category)
            except Exception as e:
                _record_register_error(row, e, "update")
        return AgResourceOutSchema.model_validate(row).model_dump(mode="json")

    @classmethod
    async def delete(cls, db: Session, ids: list[int]) -> None:
        if not ids:
            raise CustomException(msg="删除失败，ID列表不能为空")
        crud = AgResourceCRUD(db)
        to_remove: list[tuple[str, str]] = []
        for id in ids:
            row = crud.get_by_id(id)
            if not row:
                raise CustomException(msg=f"删除失败，ID={id} 的数据不存在", status_code=404)
            if row.category in ("agent", "team"):
                to_remove.append((str(row.uuid), row.category))
        crud.delete(ids)
        db.commit()
        for uuid, category in to_remove:
            try:
                _remove_from_registry(uuid, category)
            except Exception as e:
                log.error(f"[Resource] registry remove failed on delete uuid={uuid}: {e}")

    @classmethod
    async def set_status(cls, db: Session, ids: list[int], status: str) -> None:
        crud = AgResourceCRUD(db)
        rows = [crud.get_by_id(id) for id in ids]
        rows = [r for r in rows if r is not None]
        crud.set_status(ids, status)
        db.commit()
        for row in rows:
            if row.category not in ("agent", "team"):
                continue
            uuid = str(row.uuid)
            refreshed = crud.get_by_id(row.id)
            if not refreshed:
                continue
            try:
                if status == "0":
                    await _build_and_register(refreshed, db)
                else:
                    _remove_from_registry(uuid, refreshed.category)
            except Exception as e:
                _record_register_error(refreshed, e, "set_status")
