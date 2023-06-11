from fastapi import APIRouter

from .datasets import router as dataset_router

router = APIRouter()
router.include_router(dataset_router, prefix="/datasets")
