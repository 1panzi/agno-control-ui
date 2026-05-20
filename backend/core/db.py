from __future__ import annotations
import uuid as _uuid_module
from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, Integer, String, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from core.config import settings


engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    pass


class EntityMixin:
    """所有业务实体表的公共字段。"""
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(
        String(64),
        default=lambda: str(_uuid_module.uuid4()),
        nullable=False,
        unique=True,
        index=True,
    )
    status: Mapped[str] = mapped_column(String(10), default="0", nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(String(255), default=None, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )


_agno_db: Any = None


def get_agno_db() -> Any:
    """返回 agno SqliteDb/PostgresDb 单例。"""
    global _agno_db
    if _agno_db is not None:
        return _agno_db

    url = settings.database_url.lower()
    if url.startswith("postgresql") or url.startswith("postgres"):
        from agno.db.postgres.postgres import PostgresDb
        _agno_db = PostgresDb(db_url=settings.database_url, id="app-db")
    else:
        from agno.db.sqlite.sqlite import SqliteDb
        _agno_db = SqliteDb(db_url=settings.database_url, id="app-db")

    return _agno_db
