from starlette.testclient import TestClient
import json
from app.main import app

client = TestClient(app)


def test_create_dataset():
    test_request_payload = {"name": "Dataset A"}

    response = client.post(
        "/api/v1/datasets", content=json.dumps(test_request_payload),)

    assert response.status_code == 201
