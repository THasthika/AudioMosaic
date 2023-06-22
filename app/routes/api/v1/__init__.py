from fastapi import APIRouter
from .datasets import router as dataset_router
from .labels import router as label_router
from .audio_samples import router as audio_sample_router

router = APIRouter()
router.include_router(dataset_router, prefix="/datasets")
router.include_router(label_router, prefix="/labels")
router.include_router(audio_sample_router, prefix="/audio-samples")
