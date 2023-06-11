from fastapi import APIRouter, Depends, status, Query, Body
from app.config.database import get_db
from app.schemas import DatasetItem, DatasetQuery, DatasetCreate
from app.services.dataset import DatasetService
from app.utils.service_result import handle_result
from typing import Annotated

router = APIRouter()


@router.get("/", response_model=list[DatasetItem],
            status_code=status.HTTP_200_OK,
            tags=["Datasets"])
async def list_datasets(page: Annotated[int, Query(ge=1)] = 1,
                        limit: Annotated[int, Query(ge=1, le=50)] = 10,
                        db: get_db = Depends()):
    query = DatasetQuery(name=None, offset=(page - 1) * limit, limit=limit)
    service = DatasetService(db)
    datasets = service.list_datasets(query)
    return handle_result(datasets)


@router.post("/", response_model=DatasetItem,
             status_code=status.HTTP_201_CREATED, tags=["Datasets"])
async def create_dataset(dataset_create: DatasetCreate, db: get_db = Depends()):
    service = DatasetService(db)
    dataset = service.create_dataset(dataset_create)
    return handle_result(dataset)
