from fastapi import APIRouter, Depends, status
from uuid import UUID

from app.config.database import get_db
from app.schemas import (
    LabelItem, LabelCreate,
    LabelUpdate
)
from app.services.label import LabelService
from app.utils.service_result import handle_result

router = APIRouter()


@router.get("/{dataset_id}", response_model=list[LabelItem],
            status_code=status.HTTP_200_OK,
            tags=["Labels"])
async def list_labels(dataset_id: UUID, db: get_db = Depends()):
    labels = LabelService(db).list_labels_by_dataset_id(dataset_id)
    return handle_result(labels)


@router.post("", response_model=LabelItem,
             status_code=status.HTTP_201_CREATED, tags=["Labels"])
async def create_label(label_create: LabelCreate,
                       db: get_db = Depends()):
    label = LabelService(db).create_label(label_create)
    return handle_result(label)


@router.patch("/label/{id}", response_model=LabelItem,
              status_code=status.HTTP_200_OK, tags=["Labels"])
async def update_label(id: UUID,
                       label_update: LabelUpdate,
                       db: get_db = Depends()):
    updated_label = LabelService(db).update_label(id, label_update)
    return handle_result(updated_label)


@router.delete("/label/{id}", response_model=LabelItem,
               status_code=status.HTTP_200_OK, tags=["Labels"])
async def delete_label(id: UUID, db: get_db = Depends()):
    deleted_label = LabelService(db).delete_label(id)
    return handle_result(deleted_label)


@router.get("/label/{id}", response_model=LabelItem,
            status_code=status.HTTP_200_OK, tags=["Labels"])
async def get_Label_by_id(id: UUID, db: get_db = Depends()):
    label = LabelService(db).get_label(id)
    return handle_result(label)
