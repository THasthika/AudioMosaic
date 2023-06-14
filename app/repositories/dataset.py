from sqlalchemy.orm import Session
from .base import BaseCRUDRepository
from app.models.dataset import Dataset


class DatasetRepository(BaseCRUDRepository):

    def __init__(self, db: Session) -> None:
        super().__init__(db, entity=Dataset)
