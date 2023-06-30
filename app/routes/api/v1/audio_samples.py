from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    BackgroundTasks,
    status,
    Query,
    HTTPException,
)
from fastapi.responses import FileResponse
from uuid import UUID
from sqlalchemy.orm import Session

from typing import Annotated

from app.config.database import get_db

from app.schemas.generics import PaginatedResponse
from app.schemas.audio_sample import AudioSampleItem
from app.schemas.audio_sample_label import (
    AudioSampleLabelCreateRequest,
    AudioSampleLabelCreate,
    AudioSampleLabelUpdate,
)
from app.utils.service_result import handle_result
from app.services.audio_sample import AudioSampleService
from app.services.audio_sample_label import AudioSampleLabelService
from app.models.audio_sample import AudioSampleApprovalStatus

router = APIRouter()


@router.post(
    "/{dataset_id}",
    status_code=status.HTTP_201_CREATED,
    tags=["Audio Samples"],
)
async def upload_audio_samples(
    dataset_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    audio_samples: list[UploadFile],
    background_tasks: BackgroundTasks,
):
    result = await AudioSampleService(db).batch_upload_audio_samples(
        dataset_id, audio_samples, background_tasks
    )
    return handle_result(result)


@router.get(
    "/{dataset_id}",
    response_model=PaginatedResponse[AudioSampleItem],
    tags=["Audio Samples"],
)
async def audio_samples(
    dataset_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    page: Annotated[int, Query(ge=1)] = 1,
):
    result = AudioSampleService(db).list_audio_samples_by_dataset_id(
        dataset_id, limit, page
    )
    return handle_result(result)


@router.get(
    "/sample/{id}",
    response_model=AudioSampleItem,
    status_code=status.HTTP_200_OK,
    tags=["Audio Samples"],
)
async def get_audio_sample_by_id(
    id: UUID, db: Annotated[Session, Depends(get_db)]
):
    result = AudioSampleService(db).get_audio_sample(id)
    return handle_result(result)


@router.patch(
    "/sample/{id}/accept",
    response_model=AudioSampleItem,
    tags=["Audio Samples"],
)
async def accept_audio_sample(
    id: UUID, db: Annotated[Session, Depends(get_db)]
):
    result = AudioSampleService(db).update_approval_status(
        id, AudioSampleApprovalStatus.ACCEPTED
    )
    return handle_result(result)


@router.patch(
    "/sample/{id}/reject",
    response_model=AudioSampleItem,
    tags=["Audio Samples"],
)
async def reject_audio_sample(
    id: UUID, db: Annotated[Session, Depends(get_db)]
):
    result = AudioSampleService(db).update_approval_status(
        id, AudioSampleApprovalStatus.REJECTED
    )
    return handle_result(result)


@router.delete(
    "/sample/{id}",
    response_model=AudioSampleItem,
    status_code=status.HTTP_200_OK,
    tags=["Audio Samples"],
)
async def delete_audio_sample(
    id: UUID,
    background_tasks: BackgroundTasks,
    db: Annotated[Session, Depends(get_db)],
):
    result = AudioSampleService(db).delete_audio_sample(id, background_tasks)
    return handle_result(result)


@router.get("/sample/{id}/data", tags=["Audio Samples"])
async def get_audio_sample_data(
    id: UUID, db: Annotated[Session, Depends(get_db)]
):
    result = AudioSampleService(db).get_audio_sample_path(id)
    if not result.success:
        return handle_result(handle_result)
    return FileResponse(result.value)


"""
Audio Sample and Label connection APIs
"""


@router.post(
    "/sample/{id}/labels",
    status_code=status.HTTP_201_CREATED,
    tags=["Audio Samples"],
)
async def create_audio_sample_label(
    id: UUID,
    db: Annotated[Session, Depends(get_db)],
    request_body: AudioSampleLabelCreateRequest,
):
    create_model = AudioSampleLabelCreate(
        is_sample_level=request_body.is_sample_level,
        start_time=request_body.start_time,
        end_time=request_body.end_time,
        label_id=request_body.label_id,
        audio_sample_id=id,
    )
    result = AudioSampleLabelService(db).create_audio_sample_label(
        create_model
    )
    return handle_result(result)


@router.delete("/sample/{id}/labels/{instance_id}", tags=["Audio Samples"])
async def delete_audio_sample_label(
    id: UUID, instance_id: UUID, db: Annotated[Session, Depends(get_db)]
):
    result = AudioSampleLabelService(db).delete_audio_sample_label(
        id, instance_id
    )
    return handle_result(result)


@router.patch("/sample/{id}/labels/{instance_id}", tags=["Audio Samples"])
async def update_audio_sample_label(
    id: UUID,
    instance_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    request_body: AudioSampleLabelUpdate,
):
    result = AudioSampleLabelService(db).update_audio_sample_label(
        id, instance_id, request_body
    )
    return handle_result(result)


@router.get("/sample/{id}/labels", tags=["Audio Samples"])
async def get_audio_sample_labels(
    id: UUID, db: Annotated[Session, Depends(get_db)]
):
    result = AudioSampleLabelService(db).get_audio_sample_labels(id)
    return handle_result(result)
