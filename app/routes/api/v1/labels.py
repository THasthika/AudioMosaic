from fastapi import APIRouter, Depends, status
from uuid import UUID
from typing import Annotated

from app.config.database import get_db
from app.schemas import LabelItem, LabelCreate, LabelUpdate
from app.repositories.label import LabelRepository
from app.services.label import LabelService
from app.utils.service_result import handle_result
from sqlalchemy.orm import Session

router = APIRouter()


def get_label_repo(db: Annotated[Session, Depends(get_db)]):
    return LabelRepository(db)


def get_label_service(
    dataset_repo: Annotated[LabelRepository, Depends(get_label_repo)]
):
    return LabelService(dataset_repo)


@router.get(
    "/{dataset_id}",
    response_model=list[LabelItem],
    status_code=status.HTTP_200_OK,
    tags=["Labels"],
)
async def list_labels(
    dataset_id: UUID,
    label_service: Annotated[LabelService, Depends(get_label_service)],
):
    labels = label_service.list_labels_by_dataset_id(dataset_id)
    return handle_result(labels)


@router.post(
    "/{dataset_id}",
    response_model=list[LabelItem],
    status_code=status.HTTP_201_CREATED,
    tags=["Labels"],
)
async def create_labels(
    dataset_id: UUID,
    label_create_list: list[LabelCreate],
    label_service: Annotated[LabelService, Depends(get_label_service)],
):
    for label in label_create_list:
        label.dataset_id = dataset_id
    labels = label_service.create_labels(label_create_list)
    return handle_result(labels)


@router.patch(
    "/label/{id}",
    response_model=LabelItem,
    status_code=status.HTTP_200_OK,
    tags=["Labels"],
)
async def update_label(
    id: UUID,
    label_update: LabelUpdate,
    label_service: Annotated[LabelService, Depends(get_label_service)],
):
    updated_label = label_service.update_label(id, label_update)
    return handle_result(updated_label)


@router.delete(
    "/label/{id}",
    response_model=LabelItem,
    status_code=status.HTTP_200_OK,
    tags=["Labels"],
)
async def delete_label(
    id: UUID,
    label_service: Annotated[LabelService, Depends(get_label_service)],
):
    deleted_label = label_service.delete_label(id)
    return handle_result(deleted_label)


@router.get(
    "/label/{id}",
    response_model=LabelItem,
    status_code=status.HTTP_200_OK,
    tags=["Labels"],
)
async def get_label_by_id(
    id: UUID,
    label_service: Annotated[LabelService, Depends(get_label_service)],
):
    label = label_service.get_label(id)
    return handle_result(label)
