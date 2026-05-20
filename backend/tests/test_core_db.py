import pytest
from sqlalchemy.orm import Session

from core.db import Base, EntityMixin, SessionLocal, engine, get_agno_db


def test_engine_connects():
    with engine.connect() as conn:
        assert conn is not None


def test_session_local():
    db = SessionLocal()
    try:
        assert isinstance(db, Session)
    finally:
        db.close()


def test_entity_mixin_fields():
    fields = {c.name for c in EntityMixin.__table_column_names__()} if hasattr(EntityMixin, "__table_column_names__") else dir(EntityMixin)
    expected = {"id", "uuid", "status", "description", "created_at", "updated_at"}
    # 检查 EntityMixin 上定义了这些注解
    annotations = {}
    for cls in EntityMixin.__mro__ if hasattr(EntityMixin, "__mro__") else [EntityMixin]:
        annotations.update(getattr(cls, "__annotations__", {}))
    for field in expected:
        assert field in annotations, f"EntityMixin 缺少字段: {field}"


def test_get_agno_db_returns_singleton():
    db1 = get_agno_db()
    db2 = get_agno_db()
    assert db1 is db2


def test_get_agno_db_has_id():
    db = get_agno_db()
    assert db.id == "app-db"
