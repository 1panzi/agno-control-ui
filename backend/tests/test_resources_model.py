import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.db import Base
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


def test_create_model_resource(db):
    row = AgResourceModel(
        name="openai-gpt4",
        category="model",
        type="openai",
        config={"id": "gpt-4o", "api_key": "sk-test"},
    )
    db.add(row)
    db.flush()
    db.refresh(row)

    assert row.id is not None
    assert row.uuid is not None
    assert row.status == "0"
    assert row.description is None
    assert row.created_at is not None
    assert row.updated_at is not None
    assert row.config["id"] == "gpt-4o"


def test_default_status_enabled(db):
    row = AgResourceModel(name="x", category="model", type="openai", config={})
    db.add(row)
    db.flush()
    assert row.status == "0"


def test_uuid_unique(db):
    r1 = AgResourceModel(name="a", category="model", type="openai", config={})
    r2 = AgResourceModel(name="b", category="model", type="openai", config={})
    db.add_all([r1, r2])
    db.flush()
    assert r1.uuid != r2.uuid


def test_tablename():
    assert AgResourceModel.__tablename__ == "ag_resources"
