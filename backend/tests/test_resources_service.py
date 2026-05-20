import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.db import Base
from resources.model import AgResourceModel
from resources.schema import AgResourceCreateSchema, AgResourceUpdateSchema, BatchSetStatus
from resources.service import AgResourceService, set_agno_registry, get_agno_registry
from core.exceptions import CustomException

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


@pytest.fixture(autouse=True)
def mock_registry():
    from agno.registry import Registry
    registry = Registry()
    set_agno_registry(registry)
    yield registry


@pytest.fixture
def model_row(db):
    row = AgResourceModel(
        name="gpt4o", category="model", type="openai",
        config={"id": "gpt-4o", "api_key": "sk-test"}, status="0",
    )
    db.add(row)
    db.flush()
    db.refresh(row)
    return row


@pytest.mark.asyncio
async def test_create_model_resource(db):
    data = AgResourceCreateSchema(name="m1", category="model", type="openai", config={"id": "gpt-4o"})
    result = await AgResourceService.create(db=db, data=data)
    assert result["name"] == "m1"
    assert result["category"] == "model"
    assert "id" in result
    assert "uuid" in result


@pytest.mark.asyncio
async def test_create_agent_registers_to_registry(db, model_row, mock_registry):
    with patch("resources.service._build_and_register", new_callable=AsyncMock) as mock_build:
        data = AgResourceCreateSchema(
            name="my-agent", category="agent", type="base",
            config={"name": "my-agent", "model": {"ref": str(model_row.uuid)}},
        )
        result = await AgResourceService.create(db=db, data=data)
        assert result["category"] == "agent"
        mock_build.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_disabled_agent_not_registered(db, model_row, mock_registry):
    with patch("resources.service._build_and_register", new_callable=AsyncMock) as mock_build:
        data = AgResourceCreateSchema(
            name="disabled-agent", category="agent", type="base",
            config={}, status="1",
        )
        await AgResourceService.create(db=db, data=data)
        mock_build.assert_not_awaited()


@pytest.mark.asyncio
async def test_detail_not_found(db):
    with pytest.raises(CustomException) as exc_info:
        await AgResourceService.detail(db=db, id=99999)
    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_detail_returns_config(db, model_row):
    result = await AgResourceService.detail(db=db, id=model_row.id)
    assert result["id"] == model_row.id
    assert result["category"] == "model"


@pytest.mark.asyncio
async def test_page_returns_items(db):
    row = AgResourceModel(name="page-test-model", category="model", type="openai", config={}, status="0")
    db.add(row)
    db.commit()
    db.refresh(row)

    class Q:
        page = 1
        page_size = 10
        name = "page-test-model"
        category = None
        type = None
        status = None

    result = await AgResourceService.page(db=db, query=Q())
    assert result["total"] >= 1
    assert any(item["id"] == row.id for item in result["items"])


@pytest.mark.asyncio
async def test_update_not_found(db):
    with pytest.raises(CustomException) as exc_info:
        await AgResourceService.update(
            db=db, id=99999,
            data=AgResourceUpdateSchema(name="x", category="model", type="openai", config={}),
        )
    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_update_model_resource(db, model_row):
    data = AgResourceUpdateSchema(name="updated", category="model", type="openai", config={"id": "gpt-4o"})
    result = await AgResourceService.update(db=db, id=model_row.id, data=data)
    assert result["name"] == "updated"


@pytest.mark.asyncio
async def test_delete_not_found(db):
    with pytest.raises(CustomException) as exc_info:
        await AgResourceService.delete(db=db, ids=[99999])
    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_delete_empty_ids(db):
    with pytest.raises(CustomException):
        await AgResourceService.delete(db=db, ids=[])


@pytest.mark.asyncio
async def test_delete_model_resource(db, model_row):
    await AgResourceService.delete(db=db, ids=[model_row.id])
    from resources.crud import AgResourceCRUD
    assert AgResourceCRUD(db).get_by_id(model_row.id) is None


@pytest.mark.asyncio
async def test_set_status(db, model_row):
    with patch("resources.service._build_and_register", new_callable=AsyncMock):
        with patch("resources.service._remove_from_registry"):
            await AgResourceService.set_status(db=db, ids=[model_row.id], status="1")
    from resources.crud import AgResourceCRUD
    row = AgResourceCRUD(db).get_by_id(model_row.id)
    assert row.status == "1"
