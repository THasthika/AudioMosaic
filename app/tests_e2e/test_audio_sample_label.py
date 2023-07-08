from starlette.testclient import TestClient
import json
from app.main import app

client = TestClient(app)

dataset_id: None | str = None
audio_sample_id: None | str = None
label_id: None | str = None

TEST_AUDIO_FILE = "test_assets/test_file.mp3"


def test_create_audio_sample_and_label():
    global dataset_id
    global label_id
    global audio_sample_id

    # Create a dataset
    test_request_payload = {"name": "Dataset with Audio Samples"}
    create_response = client.post(
        "/api/v1/datasets",
        content=json.dumps(test_request_payload),
    )
    assert create_response.status_code == 201
    dataset_id = create_response.json()["id"]

    # create label
    label_payload = [
        {"name": "Label A", "color": "#000"},
    ]
    create_response = client.post(
        f"/api/v1/labels/{dataset_id}", content=json.dumps(label_payload)
    )
    assert create_response.status_code == 201
    label_id = create_response.json()[0]["id"]

    # create audio sample
    with open(TEST_AUDIO_FILE, "rb") as f:
        response = client.post(
            f"/api/v1/audio-samples/{dataset_id}", files={"audio_samples": f}
        )

    assert response.status_code == 201
    audio_sample_id = response.json()[0]["id"]


def test_create_audio_sample_label():
    test_payload = {"label_id": label_id, "is_sample_level": True}
    response = client.post(
        f"/api/v1/audio-samples/sample/{audio_sample_id}/labels",
        content=json.dumps(test_payload),
    )
    assert response.status_code == 201


def test_update_audio_sample_label():
    test_payload = {"label_id": label_id, "is_sample_level": True}
    response = client.post(
        f"/api/v1/audio-samples/sample/{audio_sample_id}/labels",
        content=json.dumps(test_payload),
    )
    assert response.status_code == 201

    audio_sample_label_id = response.json()["id"]
    test_payload = {
        "label_id": label_id,
        "is_sample_level": False,
        "start_time": 0,
        "end_time": 1,
    }
    response = client.patch(
        f"/api/v1/audio-samples/sample/{audio_sample_id}/labels/{audio_sample_label_id}",
        content=json.dumps(test_payload),
    )
    assert response.status_code == 200


def test_get_audio_sample_labels():
    response = client.get(
        f"/api/v1/audio-samples/sample/{audio_sample_id}/labels"
    )
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_delete_audio_sample_labels():
    response = client.get(
        f"/api/v1/audio-samples/sample/{audio_sample_id}/labels"
    )
    assert response.status_code == 200
    assert len(response.json()) > 0

    audio_sample_label_id = response.json()[0]["id"]
    response = client.delete(
        f"/api/v1/audio-samples/sample/{audio_sample_id}/labels/{audio_sample_label_id}"
    )
    assert response.status_code == 200

    response = client.delete(
        f"/api/v1/audio-samples/sample/{audio_sample_id}/labels/{audio_sample_label_id}"
    )
    assert response.status_code == 404
