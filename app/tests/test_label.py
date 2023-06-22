from starlette.testclient import TestClient
import json
from app.main import app

client = TestClient(app)

dataset_id: None | str = None


def test_create_label():
    global dataset_id

    # Create a dataset
    test_request_payload = {"name": "Dataset with Labels"}
    create_response = client.post(
        "/api/v1/datasets",
        content=json.dumps(test_request_payload),
    )
    assert create_response.status_code == 201
    dataset_id = create_response.json()["id"]

    test_request_payload = [{"name": "Label A", "color": "#000"}]

    response = client.post(
        f"/api/v1/labels/{dataset_id}",
        content=json.dumps(test_request_payload),
    )

    assert response.status_code == 201
    assert response.json()[0]["name"] == test_request_payload[0]["name"]


def test_list_labels():
    # Create a label
    test_request_payload = [
        {"name": "Label B", "color": "#f00", "description": "Hello"}
    ]
    create_response = client.post(
        f"/api/v1/labels/{dataset_id}",
        content=json.dumps(test_request_payload),
    )
    assert create_response.status_code == 201

    # List labels
    response = client.get(f"/api/v1/labels/{dataset_id}")
    assert response.status_code == 200

    # Check if the response contains at least one label
    labels = response.json()
    assert len(labels) >= 1


def test_get_label():
    # Create a label
    test_request_payload = [
        {"name": "Label C", "color": "#f00", "description": "Hello"}
    ]
    create_response = client.post(
        f"/api/v1/labels/{dataset_id}",
        content=json.dumps(test_request_payload),
    )
    assert create_response.status_code == 201
    label_id = create_response.json()[0]["id"]

    # Get the created label
    response = client.get(f"/api/v1/labels/label/{label_id}")
    assert response.status_code == 200


def test_update_label():
    # Create a label
    test_request_payload = [
        {"name": "Label D", "color": "#f00", "description": "Hello"}
    ]
    create_response = client.post(
        f"/api/v1/labels/{dataset_id}",
        content=json.dumps(test_request_payload),
    )
    assert create_response.status_code == 201
    label_id = create_response.json()[0]["id"]

    # Update the label
    update_payload = {"name": "Updated Label D"}
    response = client.patch(
        f"/api/v1/labels/label/{label_id}", content=json.dumps(update_payload)
    )
    assert response.status_code == 200

    # Check if the title name is updated
    label = response.json()
    assert label["name"] == update_payload["name"]


def test_delete_label():
    # Create a label
    test_request_payload = [
        {"name": "Label E", "color": "#f00", "description": "Hello"}
    ]
    create_response = client.post(
        f"/api/v1/labels/{dataset_id}",
        content=json.dumps(test_request_payload),
    )
    assert create_response.status_code == 201
    label_id = create_response.json()[0]["id"]

    # Delete the label
    response = client.delete(f"/api/v1/labels/label/{label_id}")
    assert response.status_code == 200

    response = client.get(f"/api/v1/labels/label/{label_id}")
    assert response.status_code == 404
