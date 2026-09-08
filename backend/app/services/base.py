from __future__ import annotations

from typing import Generic, TypeVar, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class ServiceBase(Generic[ModelType]):
    """Base service class with common CRUD operations."""

    def __init__(self, db: Session, model: type[ModelType]):
        self._db = db
        self._model = model

    def get(self, id: uuid.UUID) -> Optional[ModelType]:
        return self._db.get(self._model, id)

    def list(self, skip: int = 0, limit: int = 100) -> list[ModelType]:
        stmt = select(self._model).offset(skip).limit(limit)
        return list(self._db.exec(stmt).all())

    def create(self, **kwargs) -> ModelType:
        instance = self._model(**kwargs)
        self._db.add(instance)
        self._db.flush()
        return instance

    def update(self, id: uuid.UUID, **kwargs) -> ModelType:
        instance = self._db.get(self._model, id)
        if instance is None:
            raise ValueError(f"{self._model.__name__} not found")
        for key, value in kwargs.items():
            setattr(instance, key, value)
        self._db.flush()
        return instance

    def delete(self, id: uuid.UUID) -> bool:
        instance = self._db.get(self._model, id)
        if instance is None:
            return False
        self._db.delete(instance)
        self._db.flush()
        return True