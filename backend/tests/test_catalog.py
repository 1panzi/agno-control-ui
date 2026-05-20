import pytest
from fastapi.testclient import TestClient

from main import _base_app


@pytest.fixture
def client():
    with TestClient(_base_app, raise_server_exceptions=False) as c:
        yield c


def test_schema_all_categories(client):
    resp = client.get("/api/v1/agno_manage/schema")
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    cats = data["data"]["category"]
    assert "model" in cats
    assert "agent" in cats


def test_schema_types_by_category(client):
    resp = client.get("/api/v1/agno_manage/schema?category=model")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["category"] == "model"
    types = [t["type"] for t in data["types"]]
    assert "openai" in types
    assert "anthropic" in types


def test_schema_fields_by_type(client):
    resp = client.get("/api/v1/agno_manage/schema?category=model&type=openai")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["category"] == "model"
    assert data["type"] == "openai"
    assert isinstance(data["fields"], list)
    assert len(data["fields"]) > 0


def test_schema_fields_agent(client):
    resp = client.get("/api/v1/agno_manage/schema?category=agent&type=base")
    assert resp.status_code == 200
    data = resp.json()["data"]
    field_names = [f["name"] for f in data["fields"]]
    assert "model" in field_names
    assert "name" in field_names


def test_schema_unknown_type_returns_404(client):
    resp = client.get("/api/v1/agno_manage/schema?category=model&type=nonexistent_xyz")
    assert resp.status_code == 404


def test_schema_embedder_types(client):
    resp = client.get("/api/v1/agno_manage/schema?category=embedder")
    assert resp.status_code == 200
    types = [t["type"] for t in resp.json()["data"]["types"]]
    assert "openai" in types


def test_schema_reader_types(client):
    resp = client.get("/api/v1/agno_manage/schema?category=reader")
    assert resp.status_code == 200
    types = [t["type"] for t in resp.json()["data"]["types"]]
    assert "pdf" in types
    assert "docx" in types
