from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_db_version():
    response = client.get("/api/db-version")
    assert response.status_code == 200
