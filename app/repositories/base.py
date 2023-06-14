from sqlalchemy.orm import Session
from app.config.database import Base
from uuid import UUID


class BaseRepository():
    def __init__(self, db: Session) -> None:
        self.db = db


class BaseCRUDRepository(BaseRepository):

    def __init__(self, db: Session, entity: Base) -> None:
        super().__init__(db)
        self.entity = entity

    def get_all(self):
        return self.db.query(self.model)

    def get_by_id(self, id: UUID):
        return self.db.query(self.entity).filter(self.entity.id == id).first()

    def add(self, entity: Base):
        self.db.add(entity)

    def update(self, entity: Base):
        pass

    # def delete(self, entity):
    #     entity.is_active = False
    #     self.update(entity)

    def permanent_delete(self, entity):
        self.db.delete(entity)
