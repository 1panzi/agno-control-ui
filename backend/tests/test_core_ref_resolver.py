import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.db import Base
from core.ref_resolver import RefResolver
from resources.model import AgResourceModel

TEST_DB_URL = "sqlite:///./test.db"
_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
_Session = sessionmaker(bind=_engine, autocommit=False, autoflush=False)


@pytest.fixture(autouse=True)
def setup_tables():
    Base.metadata.create_all(_engine)
    yield


@pytest.fixture
def db():
    session = _Session()
    try:
        yield session
        session.rollback()
    finally:
        session.close()


@pytest.fixture
def model_row(db):
    row = AgResourceModel(
        name="test-model",
        category="model",
        type="openai",
        config={"id": "gpt-4o", "api_key": "sk-test"},
        status="0",
    )
    db.add(row)
    db.flush()
    db.refresh(row)
    return row


@pytest.mark.asyncio
async def test_resolve_none(db):
    resolver = RefResolver(db=db)
    result = await resolver.resolve(None)
    assert result is None


@pytest.mark.asyncio
async def test_resolve_list_empty(db):
    resolver = RefResolver(db=db)
    result = await resolver.resolve_list(None)
    assert result == []

    result = await resolver.resolve_list([])
    assert result == []


@pytest.mark.asyncio
async def test_resolve_ref_not_found(db):
    resolver = RefResolver(db=db)
    with pytest.raises(ValueError, match="not found or disabled"):
        await resolver.resolve({"ref": "00000000-0000-0000-0000-000000000000"})


@pytest.mark.asyncio
async def test_resolve_ref_disabled(db, model_row):
    model_row.status = "1"
    db.flush()
    resolver = RefResolver(db=db)
    with pytest.raises(ValueError, match="not found or disabled"):
        await resolver.resolve({"ref": str(model_row.uuid)})


@pytest.mark.asyncio
async def test_resolve_inline_missing_fields(db):
    resolver = RefResolver(db=db)
    with pytest.raises(ValueError, match="must have 'category' and 'type'"):
        await resolver.resolve({"name": "foo"})


@pytest.mark.asyncio
async def test_resolve_inline_no_builder(db):
    resolver = RefResolver(db=db)
    with pytest.raises(ValueError, match="No builder registered"):
        await resolver.resolve({"category": "unknown_cat", "type": "unknown_type"})


@pytest.mark.asyncio
async def test_resolve_ref_cached(db, model_row):
    """同一 uuid 第二次 resolve 应命中缓存（不再查库）。"""
    from unittest.mock import patch, MagicMock

    mock_obj = MagicMock()
    resolver = RefResolver(db=db)
    uuid = str(model_row.uuid)

    with patch("builders.builder_registry.builder_registry") as mock_reg:
        mock_builder = MagicMock()
        mock_builder.build.return_value = mock_obj
        mock_reg.get.return_value = mock_builder

        result1 = await resolver.resolve({"ref": uuid})
        result2 = await resolver.resolve({"ref": uuid})

    assert result1 is result2
    assert mock_builder.build.call_count == 1
