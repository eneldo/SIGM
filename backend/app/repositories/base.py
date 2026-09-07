from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any, TypeVar

from sqlalchemy import Select, select

from app.models.base import TenantModel

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType", bound=TenantModel)


class BaseRepository[ModelType: TenantModel]:
    def __init__(self, model: type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    def _base_query(self, tenant_id: str | uuid.UUID) -> Select:
        return select(self.model).where(self.model.tenant_id == uuid.UUID(tenant_id))

    async def get_by_id(self, tenant_id: str | uuid.UUID, id: uuid.UUID) -> ModelType | None:
        result = await self.db.execute(
            self._base_query(tenant_id).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_multi(
        self,
        tenant_id: str | uuid.UUID,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: dict[str, Any] | None = None,
    ) -> Sequence[ModelType]:
        query = self._base_query(tenant_id)
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field) and value is not None:
                    query = query.where(getattr(self.model, field) == value)
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def count(self, tenant_id: str | uuid.UUID, filters: dict[str, Any] | None = None) -> int:
        from sqlalchemy import func

        query = select(func.count()).select_from(self.model).where(
            self.model.tenant_id == uuid.UUID(tenant_id)
        )
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field) and value is not None:
                    query = query.where(getattr(self.model, field) == value)
        result = await self.db.execute(query)
        return result.scalar_one()

    async def create(self, tenant_id: str | uuid.UUID, **kwargs: Any) -> ModelType:
        obj = self.model(tenant_id=uuid.UUID(tenant_id), **kwargs)
        self.db.add(obj)
        await self.db.flush()
        await self.db.refresh(obj)
        return obj

    async def update(self, tenant_id: str | uuid.UUID, id: uuid.UUID, **kwargs: Any) -> ModelType | None:
        obj = await self.get_by_id(tenant_id, id)
        if obj is None:
            return None
        for field, value in kwargs.items():
            if hasattr(obj, field):
                setattr(obj, field, value)
        await self.db.flush()
        await self.db.refresh(obj)
        return obj

    async def delete(self, tenant_id: str | uuid.UUID, id: uuid.UUID) -> bool:
        obj = await self.get_by_id(tenant_id, id)
        if obj is None:
            return False
        await self.db.delete(obj)
        return True
