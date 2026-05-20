"""
DB builders build() 测试。
"""
import pytest
from unittest.mock import MagicMock

from builders.dbs.sqlite import SqliteDbBuilder
from builders.dbs.in_memory import InMemoryDbBuilder


@pytest.fixture
def resolver():
    return MagicMock()


@pytest.mark.asyncio
async def test_sqlite_build_with_url(resolver):
    builder = SqliteDbBuilder()
    obj = await builder.build({"db_url": "sqlite:///./test.db"}, resolver)
    from agno.db.sqlite.sqlite import SqliteDb
    assert isinstance(obj, SqliteDb)


@pytest.mark.asyncio
async def test_sqlite_build_with_file(resolver):
    builder = SqliteDbBuilder()
    obj = await builder.build({"db_file": "/tmp/test_agno.db"}, resolver)
    from agno.db.sqlite.sqlite import SqliteDb
    assert isinstance(obj, SqliteDb)


@pytest.mark.asyncio
async def test_sqlite_build_empty_config(resolver):
    builder = SqliteDbBuilder()
    obj = await builder.build({}, resolver)
    from agno.db.sqlite.sqlite import SqliteDb
    assert isinstance(obj, SqliteDb)


@pytest.mark.asyncio
async def test_sqlite_build_custom_tables(resolver):
    builder = SqliteDbBuilder()
    obj = await builder.build({
        "db_url": "sqlite:///./test.db",
        "session_table": "my_sessions",
        "memory_table": "my_memories",
    }, resolver)
    assert obj.session_table_name == "my_sessions"
    assert obj.memory_table_name == "my_memories"


@pytest.mark.asyncio
async def test_in_memory_build(resolver):
    builder = InMemoryDbBuilder()
    obj = await builder.build({}, resolver)
    from agno.db.in_memory.in_memory_db import InMemoryDb
    assert isinstance(obj, InMemoryDb)


@pytest.mark.asyncio
async def test_in_memory_build_with_tables(resolver):
    builder = InMemoryDbBuilder()
    obj = await builder.build({"session_table": "custom_sessions"}, resolver)
    from agno.db.in_memory.in_memory_db import InMemoryDb
    assert isinstance(obj, InMemoryDb)


def test_db_category_and_types():
    assert SqliteDbBuilder.category == "db"
    assert SqliteDbBuilder.type == "sqlite"
    assert InMemoryDbBuilder.category == "db"
    assert InMemoryDbBuilder.type == "in_memory"


def test_sqlite_schema_has_db_url():
    builder = SqliteDbBuilder()
    names = [f["name"] for f in builder.schema]
    assert "db_url" in names or "db_file" in names
