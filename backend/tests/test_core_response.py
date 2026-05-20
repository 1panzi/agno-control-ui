import pytest
from core.response import R


def test_r_ok_default():
    r = R.ok()
    assert r.code == 0
    assert r.message == "ok"
    assert r.data is None


def test_r_ok_with_data():
    r = R.ok(data={"key": "value"}, message="success")
    assert r.code == 0
    assert r.message == "success"
    assert r.data == {"key": "value"}


def test_r_fail():
    r = R.fail(code=404, message="not found")
    assert r.code == 404
    assert r.message == "not found"
    assert r.data is None


def test_r_model_dump():
    r = R.ok(data=42)
    d = r.model_dump()
    assert d["code"] == 0
    assert d["data"] == 42
    assert "message" in d
