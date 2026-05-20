import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.db import Base
from resources.crud import AgResourceCRUD
from resources.model import AgResourceModel
from resources.schema import AgResourceCreateSchema, AgResourceUpdateSchema

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
def crud(db):
    return AgResourceCRUD(db)


@pytest.fixture
def sample_row(db):
    row = AgResourceModel(
        name="test-model",
        category="model",
        type="openai",
        config={"id": "gpt-4o"},
        status="0",
    )
    db.add(row)
    db.flush()
    db.refresh(row)
    return row


def test_create(crud, db):
    data = AgResourceCreateSchema(name="new-model", category="model", type="openai", config={"id": "gpt-4o"})
    row = crud.create(data)
    assert row.id is not None
    assert row.name == "new-model"
    assert row.category == "model"


def test_get_by_id(crud, sample_row):
    row = crud.get_by_id(sample_row.id)
    assert row is not None
    assert row.id == sample_row.id


def test_get_by_id_not_found(crud):
    assert crud.get_by_id(99999) is None


def test_get_by_uuid(crud, sample_row):
    row = crud.get_by_uuid(sample_row.uuid)
    assert row is not None
    assert row.uuid == sample_row.uuid


def test_get_by_uuid_not_found(crud):
    assert crud.get_by_uuid("nonexistent-uuid") is None


def test_list_enabled(crud, db):
    db.add(AgResourceModel(name="enabled", category="model", type="openai", config={}, status="0"))
    db.add(AgResourceModel(name="disabled", category="model", type="openai", config={}, status="1"))
    db.flush()
    rows = crud.list_enabled()
    names = [r.name for r in rows]
    assert "enabled" in names
    assert "disabled" not in names


def test_list_enabled_by_category(crud, db):
    db.add(AgResourceModel(name="m1", category="model", type="openai", config={}, status="0"))
    db.add(AgResourceModel(name="a1", category="agent", type="base", config={}, status="0"))
    db.flush()
    rows = crud.list_enabled(category="agent")
    assert all(r.category == "agent" for r in rows)


def test_page_basic(crud, db):
    for i in range(5):
        db.add(AgResourceModel(name=f"row-{i}", category="model", type="openai", config={}, status="0"))
    db.flush()
    result = crud.page(page=1, page_size=3)
    assert result["total"] >= 5
    assert len(result["items"]) == 3
    assert result["has_next"] is True


def test_page_filter_by_name(crud, db):
    db.add(AgResourceModel(name="unique-xyz", category="model", type="openai", config={}, status="0"))
    db.flush()
    result = crud.page(page=1, page_size=10, name="unique-xyz")
    assert result["total"] >= 1
    assert all("unique-xyz" in r.name for r in result["items"])


def test_page_filter_by_category(crud, db):
    db.add(AgResourceModel(name="agent-only", category="agent", type="base", config={}, status="0"))
    db.flush()
    result = crud.page(page=1, page_size=10, category="agent")
    assert all(r.category == "agent" for r in result["items"])


def test_update(crud, sample_row):
    data = AgResourceUpdateSchema(name="updated-name", category="model", type="openai", config={})
    row = crud.update(sample_row.id, data)
    assert row.name == "updated-name"


def test_update_not_found(crud):
    data = AgResourceUpdateSchema(name="x", category="model", type="openai", config={})
    result = crud.update(99999, data)
    assert result is None


def test_delete(crud, db):
    row = AgResourceModel(name="to-delete", category="model", type="openai", config={})
    db.add(row)
    db.flush()
    id_ = row.id
    crud.delete([id_])
    assert crud.get_by_id(id_) is None


def test_set_status(crud, sample_row):
    crud.set_status([sample_row.id], "1")
    db_row = crud.get_by_id(sample_row.id)
    assert db_row.status == "1"
