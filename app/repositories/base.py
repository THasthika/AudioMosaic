from sqlalchemy.orm import Session
from uuid import UUID
from abc import abstractmethod


class BaseRepository():
    def __init__(self, db: Session) -> None:
        self.db = db


class BaseCRUDRepository(BaseRepository):

    ModelType = NotImplementedError
    ModelCreateType = NotImplementedError
    ModelUpdateType = NotImplementedError

    ItemNotFoundException = NotImplementedError

    def __init__(self, db: Session, entity: ModelType) -> None:
        super().__init__(db)
        self.entity = entity

    @abstractmethod
    def get_model_from_create_type(self,
                                   create_type: ModelCreateType) -> ModelType:
        raise NotImplementedError()

    @abstractmethod
    def get_model_from_update_type(self,
                                   current_model: ModelType,
                                   update_model: ModelUpdateType) -> ModelType:
        raise NotImplementedError()

    def get_all(self):
        items = self.db.query(self.model)
        return items

    def get_by_id(self, id: UUID):
        item = self.db.query(self.entity).filter(self.entity.id == id).first()
        return item

    def create(self, create_type: ModelCreateType):
        entity = self.get_model_from_create_type(create_type)
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def update(self, id: UUID, update_type: ModelUpdateType):
        current_model = self.get_by_id(id)
        if current_model is None:
            raise self.ItemNotFoundException()
        updated_model = self.get_model_from_update_type(
            current_model, update_type)
        self.db.commit()
        self.db.refresh(updated_model)
        return updated_model

    # def delete(self, entity):
    #     entity.is_active = False
    #     self.update(entity)

    def delete(self, id: UUID):
        item = self.get_by_id(id)
        if item is None:
            return self.ItemNotFoundException()
        self.db.delete(item)
        self.db.commit()
        return item
