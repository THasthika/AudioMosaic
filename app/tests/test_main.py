from starlette.testclient import TestClient

from app.main import app

import pytest
pytest.skip(allow_module_level=True)

client = TestClient(app)


def test_db_version():
    response = client.get("/api/db-version")
    assert response.status_code == 200
