from starlette.testclient import TestClient
import json
from app.main import app

import pytest
pytest.skip(allow_module_level=True)

client = TestClient(app)

dataset_id: None | str = None

TEST_AUDIO_FILE = "test_assets/test_file.mp3"


def test_create_audio_sample():
    global dataset_id

    # Create a dataset
    test_request_payload = {"name": "Dataset with Audio Samples"}
    create_response = client.post(
        "/api/v1/datasets",
        content=json.dumps(test_request_payload),
    )
    assert create_response.status_code == 201
    dataset_id = create_response.json()["id"]

    with open(TEST_AUDIO_FILE, "rb") as f:
        response = client.post(
            f"/api/v1/audio-samples/{dataset_id}", files={"audio_samples": f}
        )

    assert response.status_code == 201


def test_list_audio_samples():
    # Create an audio sample
    with open(TEST_AUDIO_FILE, "rb") as f:
        create_response = client.post(
            f"/api/v1/audio-samples/{dataset_id}", files={"audio_samples": f}
        )
    assert create_response.status_code == 201

    # List audio samples
    response = client.get(f"/api/v1/audio-samples/{dataset_id}")
    assert response.status_code == 200

    # Check if the response contains at least one audio sample
    response_data = response.json()
    audio_samples = response_data["items"]
    assert response_data["total"] > 0
    assert len(audio_samples) >= 1


def test_get_audio_sample():
    # Create an audio sample
    with open(TEST_AUDIO_FILE, "rb") as f:
        create_response = client.post(
            f"/api/v1/audio-samples/{dataset_id}", files={"audio_samples": f}
        )
    assert create_response.status_code == 201

    audio_sample_id = create_response.json()[0]["id"]

    # Get the created audio sample
    response = client.get(f"/api/v1/audio-samples/sample/{audio_sample_id}")
    assert response.status_code == 200


def test_update_approval_status():
    # Create am audio sample
    with open(TEST_AUDIO_FILE, "rb") as f:
        create_response = client.post(
            f"/api/v1/audio-samples/{dataset_id}", files={"audio_samples": f}
        )
    assert create_response.status_code == 201

    audio_sample_id = create_response.json()[0]["id"]

    # approve an audio sample
    response = client.patch(
        f"/api/v1/audio-samples/sample/{audio_sample_id}/accept"
    )

    assert response.status_code == 200
    assert response.json()["approval_status"] == "ACCEPTED"

    # reject an audio sample
    response = client.patch(
        f"/api/v1/audio-samples/sample/{audio_sample_id}/reject"
    )

    assert response.status_code == 200
    assert response.json()["approval_status"] == "REJECTED"


def test_delete_audio_sample():
    # Create an audio sample
    with open(TEST_AUDIO_FILE, "rb") as f:
        create_response = client.post(
            f"/api/v1/audio-samples/{dataset_id}", files={"audio_samples": f}
        )
    assert create_response.status_code == 201

    audio_sample_id = create_response.json()[0]["id"]

    # Delete the audio sample
    response = client.delete(f"/api/v1/audio-samples/sample/{audio_sample_id}")
    assert response.status_code == 200

    response = client.get(f"/api/v1/audio-samples/sample/{audio_sample_id}")
    assert response.status_code == 404


def test_audio_sample_data_retrieval():
    # Create an audio sample
    with open(TEST_AUDIO_FILE, "rb") as f:
        create_response = client.post(
            f"/api/v1/audio-samples/{dataset_id}", files={"audio_samples": f}
        )
    assert create_response.status_code == 201

    audio_sample_id = create_response.json()[0]["id"]

    # Get audio data
    response = client.get(
        f"/api/v1/audio-samples/sample/{audio_sample_id}/data"
    )
    assert response.status_code == 200
