import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import AsyncMock, patch

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


@pytest.fixture
def client(db):
    from main import _base_app
    from resources.controller import get_db
    from resources.service import set_agno_registry
    from agno.registry import Registry

    set_agno_registry(Registry())
    _base_app.dependency_overrides[get_db] = lambda: db
    with TestClient(_base_app, raise_server_exceptions=False) as c:
        yield c
    _base_app.dependency_overrides.clear()


@pytest.fixture
def model_row(db):
    row = AgResourceModel(
        name="gpt4o", category="model", type="openai",
        config={"id": "gpt-4o", "api_key": "sk-test"}, status="0",
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def test_list_empty(client):
    resp = client.get("/api/v1/agno_manage/resources/list")
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    assert data["data"]["total"] >= 0


def test_list_with_filters(client, model_row):
    resp = client.get("/api/v1/agno_manage/resources/list?category=model&status=0")
    assert resp.status_code == 200
    items = resp.json()["data"]["items"]
    assert any(i["id"] == model_row.id for i in items)


def test_detail_found(client, model_row):
    resp = client.get(f"/api/v1/agno_manage/resources/detail/{model_row.id}")
    assert resp.status_code == 200
    assert resp.json()["data"]["id"] == model_row.id


def test_detail_not_found(client):
    resp = client.get("/api/v1/agno_manage/resources/detail/99999")
    assert resp.status_code in (400, 404)


def test_create_resource(client):
    with patch("resources.service._build_and_register", new_callable=AsyncMock):
        resp = client.post("/api/v1/agno_manage/resources/create", json={
            "name": "new-model",
            "category": "model",
            "type": "openai",
            "config": {"id": "gpt-4o"},
        })
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["name"] == "new-model"
    assert data["uuid"] is not None


def test_create_missing_required_field(client):
    resp = client.post("/api/v1/agno_manage/resources/create", json={"name": "x"})
    assert resp.status_code == 422


def test_update_resource(client, model_row):
    resp = client.put(f"/api/v1/agno_manage/resources/update/{model_row.id}", json={
        "name": "updated",
        "category": "model",
        "type": "openai",
        "config": {},
    })
    assert resp.status_code == 200
    assert resp.json()["data"]["name"] == "updated"


def test_update_not_found(client):
    resp = client.put("/api/v1/agno_manage/resources/update/99999", json={
        "name": "x",
        "category": "model",
        "type": "openai",
        "config": {},
    })
    assert resp.status_code in (400, 404)


def test_delete_resource(client, model_row):
    resp = client.request(
        "DELETE",
        "/api/v1/agno_manage/resources/delete",
        json=[model_row.id],
    )
    assert resp.status_code == 200
    assert "删除" in resp.json()["msg"]


def test_set_status(client, model_row):
    resp = client.patch("/api/v1/agno_manage/resources/status", json={
        "ids": [model_row.id],
        "status": "1",
    })
    assert resp.status_code == 200


def test_pagination(client, db):
    for i in range(5):
        db.add(AgResourceModel(name=f"page-item-{i}", category="model", type="openai", config={}, status="0"))
    db.commit()
    resp = client.get("/api/v1/agno_manage/resources/list?page=1&page_size=2")
    data = resp.json()["data"]
    assert len(data["items"]) == 2
