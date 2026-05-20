import pytest
from pydantic import ValidationError
from resources.schema import (
    AgResourceCreateSchema,
    AgResourceUpdateSchema,
    AgResourceOutSchema,
    BatchSetStatus,
)
from datetime import datetime


def test_create_schema_required_fields():
    with pytest.raises(ValidationError):
        AgResourceCreateSchema()


def test_create_schema_valid():
    s = AgResourceCreateSchema(name="gpt4", category="model", type="openai")
    assert s.name == "gpt4"
    assert s.config == {}
    assert s.status == "0"
    assert s.description is None


def test_create_schema_with_config():
    s = AgResourceCreateSchema(
        name="gpt4",
        category="model",
        type="openai",
        config={"id": "gpt-4o"},
    )
    assert s.config["id"] == "gpt-4o"


def test_create_schema_name_max_length():
    with pytest.raises(ValidationError):
        AgResourceCreateSchema(name="x" * 256, category="model", type="openai")


def test_update_schema_inherits_create():
    s = AgResourceUpdateSchema(name="n", category="agent", type="base")
    assert isinstance(s, AgResourceCreateSchema)


def test_out_schema_from_attributes():
    now = datetime.now()
    s = AgResourceOutSchema(
        name="n",
        category="model",
        type="openai",
        id=1,
        uuid="abc-123",
        created_at=now,
        updated_at=now,
    )
    assert s.id == 1
    assert s.uuid == "abc-123"


def test_batch_set_status_valid():
    b = BatchSetStatus(ids=[1, 2, 3], status="1")
    assert b.ids == [1, 2, 3]
    assert b.status == "1"


def test_batch_set_status_missing_fields():
    with pytest.raises(ValidationError):
        BatchSetStatus()
