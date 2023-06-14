from starlette.testclient import TestClient
import json
from app.main import app

client = TestClient(app)


def test_create_dataset():
    test_request_payload = {"name": "Dataset A"}

    response = client.post(
        "/api/v1/datasets",
        content=json.dumps(test_request_payload),
    )

    assert response.status_code == 201
    # Add additional assertions to validate the response body, if necessary


def test_list_datasets():
    # Create a dataset
    test_request_payload = {"name": "Dataset B"}
    create_response = client.post(
        "/api/v1/datasets",
        content=json.dumps(test_request_payload),
    )
    assert create_response.status_code == 201

    # List datasets
    response = client.get("/api/v1/datasets")
    assert response.status_code == 200

    # Check if the response contains at least one dataset
    datasets = response.json()
    assert len(datasets) >= 1


def test_get_dataset():
    # Create a dataset
    test_request_payload = {"name": "Dataset C"}
    create_response = client.post(
        "/api/v1/datasets",
        content=json.dumps(test_request_payload),
    )
    assert create_response.status_code == 201
    dataset_id = create_response.json()["id"]

    # Get the created dataset
    response = client.get(f"/api/v1/datasets/{dataset_id}")
    assert response.status_code == 200


def test_update_dataset():
    # Create a dataset
    test_request_payload = {"name": "Dataset D"}
    create_response = client.post(
        "/api/v1/datasets",
        content=json.dumps(test_request_payload),
    )
    assert create_response.status_code == 201
    dataset_id = create_response.json()["id"]

    # Update the dataset
    update_payload = {"name": "Updated Dataset D"}
    response = client.patch(
        f"/api/v1/datasets/{dataset_id}", content=json.dumps(update_payload)
    )
    assert response.status_code == 200

    # Check if the title name is updated
    dataset = response.json()
    assert dataset["name"] == update_payload["name"]


def test_delete_dataset():
    # Create a dataset
    test_request_payload = {"name": "Dataset E"}
    create_response = client.post(
        "/api/v1/datasets",
        content=json.dumps(test_request_payload),
    )
    assert create_response.status_code == 201
    dataset_id = create_response.json()["id"]

    # Delete the dataset
    response = client.delete(f"/api/v1/datasets/{dataset_id}")
    assert response.status_code == 200

    response = client.get(f"/api/v1/datasets/{dataset_id}")
    assert response.status_code == 404
