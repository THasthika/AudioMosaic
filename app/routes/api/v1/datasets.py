from fastapi import APIRouter, Depends, status, Query
from uuid import UUID

from app.config.database import get_db
from app.schemas import DatasetItem, DatasetQuery, DatasetCreate, DatasetUpdate
from app.schemas.generics import PaginatedResponse
from app.repositories.dataset import DatasetRepository
from app.services.dataset import DatasetService
from app.utils.service_result import handle_result
from typing import Annotated
from sqlalchemy.orm import Session

router = APIRouter()


def get_dataset_repo(db: Annotated[Session, Depends(get_db)]):
    return DatasetRepository(db)


def get_dataset_service(
    dataset_repo: Annotated[DatasetRepository, Depends(get_dataset_repo)]
):
    return DatasetService(dataset_repo)


@router.get(
    "",
    response_model=PaginatedResponse[DatasetItem],
    status_code=status.HTTP_200_OK,
    tags=["Datasets"],
)
async def list_datasets(
    dataset_service: Annotated[DatasetService, Depends(get_dataset_service)],
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
):
    query = DatasetQuery(name=None, offset=(page - 1) * limit, limit=limit)
    datasets = dataset_service.list_datasets(query)
    return handle_result(datasets)


@router.post(
    "",
    response_model=DatasetItem,
    status_code=status.HTTP_201_CREATED,
    tags=["Datasets"],
)
async def create_dataset(
    dataset_create: DatasetCreate,
    dataset_service: Annotated[DatasetService, Depends(get_dataset_service)],
):
    dataset = dataset_service.create_dataset(dataset_create)
    return handle_result(dataset)


@router.patch(
    "/{id}",
    response_model=DatasetItem,
    status_code=status.HTTP_200_OK,
    tags=["Datasets"],
)
async def update_dataset(
    id: UUID,
    dataset_update: DatasetUpdate,
    dataset_service: Annotated[DatasetService, Depends(get_dataset_service)],
):
    updated_dataset = dataset_service.update_dataset(id, dataset_update)
    return handle_result(updated_dataset)


@router.delete(
    "/{id}",
    response_model=DatasetItem,
    status_code=status.HTTP_200_OK,
    tags=["Datasets"],
)
async def delete_dataset(
    id: UUID,
    dataset_service: Annotated[DatasetService, Depends(get_dataset_service)],
):
    deleted_dataset = dataset_service.delete_dataset(id)
    return handle_result(deleted_dataset)


@router.get(
    "/{id}",
    response_model=DatasetItem,
    status_code=status.HTTP_200_OK,
    tags=["Datasets"],
)
async def get_dataset_by_id(
    id: UUID,
    dataset_service: Annotated[DatasetService, Depends(get_dataset_service)],
):
    dataset = dataset_service.get_dataset(id)
    return handle_result(dataset)
