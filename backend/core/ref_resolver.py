"""
RefResolver — 统一处理 ref/inline/override 三种资源引用模式。

支持的 value 格式：
  - None                         → return None
  - {"ref": "uuid"}              → 查 ag_resources，展开 config，递归 build
  - {"ref": "uuid", "override": {...}} → 查表，merge override，build
  - {"category": ..., "type": ..., ...} → inline，直接 build

缓存策略：
  - 无 override：cache_key = uuid
  - 有 override：cache_key = f"{uuid}:{hash(str(sorted(override.items())))}"

注意：内部数据库查询使用同步 Session，resolve() 保持 async def 供 builder await。
"""

import inspect
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from resources.model import AgResourceModel


class RefResolver:
    def __init__(self, db: Session):
        self.db = db
        self._cache: dict[str, Any] = {}

    async def resolve(self, value: dict | None) -> Any:
        if value is None:
            return None

        if "ref" in value:
            uuid = value["ref"]
            override = value.get("override") or {}

            cache_key = f"{uuid}:{hash(str(sorted(override.items())))}" if override else uuid

            if cache_key in self._cache:
                return self._cache[cache_key]

            result = self.db.execute(
                select(AgResourceModel).where(
                    AgResourceModel.uuid == uuid,
                    AgResourceModel.status == "0",
                )
            )
            row = result.scalar_one_or_none()
            if row is None:
                raise ValueError(f"Resource {uuid} not found or disabled")

            config = {**(row.config or {}), **override}

            from builders.builder_registry import builder_registry
            builder = builder_registry.get((row.category, row.type))
            if builder is None:
                raise ValueError(
                    f"No builder registered for category={row.category}, type={row.type}"
                )

            obj = builder.build(config, self)
            if inspect.iscoroutine(obj):
                obj = await obj
            self._cache[cache_key] = obj
            return obj

        value = dict(value)
        category = value.pop("category", None)
        type_ = value.pop("type", None)
        if category is None or type_ is None:
            raise ValueError(
                f"Inline resource must have 'category' and 'type' fields, got: {list(value.keys())}"
            )

        from builders.builder_registry import builder_registry
        builder = builder_registry.get((category, type_))
        if builder is None:
            raise ValueError(
                f"No builder registered for category={category}, type={type_}"
            )

        obj = builder.build(value, self)
        if inspect.iscoroutine(obj):
            obj = await obj
        return obj

    async def resolve_list(self, values: list | None) -> list:
        if not values:
            return []
        results = []
        for v in values:
            obj = await self.resolve(v)
            if obj is not None:
                results.append(obj)
        return results
