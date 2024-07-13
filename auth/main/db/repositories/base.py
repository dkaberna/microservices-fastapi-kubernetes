from typing import Generic, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from fastapi import status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from main.core.logger import logger

from main.db.base_class import Base

from main.core.exceptions import BaseInternalException

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base repository with basic methods.
    """

    def __init__(self, db: Session, model: Type[ModelType]) -> None:
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        :param db: A SQLAlchemy Session object.
        :param model: A SQLAlchemy model class.
        """
        self.db = db
        self.model = model

    def get_all(self) -> List[ModelType]:
        """
        Return all objects from specific db table.
        """
        try:
            return self.db.query(self.model).all()
        except Exception as e:
            logger.error("Exception occurred: %s", e)
            raise BaseInternalException(
                message="Error in get_all function", status_code=status.HTTP_400_BAD_REQUEST
            )

    def get(self, obj_id: str) -> Optional[ModelType]:
        """
        Get object by `id` field.
        """
        try:
            return self.db.query(self.model).filter(self.model.id == obj_id).first()
        except Exception as e:
            logger.error("Exception occurred: %s", e)
            raise BaseInternalException(
                message="Error in get function", status_code=status.HTTP_400_BAD_REQUEST
            )

    def create(self, obj_create: CreateSchemaType) -> ModelType:
        """
        Create new object in db table.
        """
        try:
            obj = self.model(**obj_create.model_dump())
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
            return obj
        except Exception as e:
            logger.error("Exception occurred: %s", e)
            raise BaseInternalException(
                message="Error in create function", status_code=status.HTTP_400_BAD_REQUEST
            )

    def update(self, obj: ModelType, obj_update: UpdateSchemaType) -> ModelType:
        """
        Update model object by fields from `obj_update` schema.
        """
        try:
            obj_data = jsonable_encoder(obj)
            update_data = obj_update.model_dump(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(obj, field, update_data[field])
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
            return obj
        except Exception as e:
            logger.error("Exception occurred: %s", e)
            raise BaseInternalException(
                message="Error in update function", status_code=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, obj_id: int) -> Optional[ModelType]:
        """
        Delete object.
        """
        try:
            obj = self.db.query(self.model).get(obj_id)
            self.db.delete(obj)
            self.db.commit()
            return obj
        except Exception as e:
            logger.error("Exception occurred: %s", e)
            raise BaseInternalException(
                message="Error in delete function", status_code=status.HTTP_400_BAD_REQUEST
            )
    