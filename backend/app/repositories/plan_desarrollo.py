from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import selectinload

from app.models.plan_desarrollo import (
    AvanceMeta,
    Indicador,
    Meta,
    NodoPlan,
    PlanDesarrollo,
    ProgramacionAnualMeta,
)
from app.repositories.base import BaseRepository

if TYPE_CHECKING:
    import uuid
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession


class PlanDesarrolloRepository(BaseRepository[PlanDesarrollo]):
    def __init__(self, db: AsyncSession):
        super().__init__(PlanDesarrollo, db)

    async def get_with_nodos(
        self, tenant_id: str | uuid.UUID, plan_id: uuid.UUID
    ) -> PlanDesarrollo | None:
        result = await self.db.execute(
            self._base_query(tenant_id)
            .where(PlanDesarrollo.id == plan_id)
            .options(selectinload(PlanDesarrollo.nodos))
        )
        return result.scalar_one_or_none()

    async def get_by_administracion(
        self, tenant_id: str | uuid.UUID, administracion_id: uuid.UUID
    ) -> Sequence[PlanDesarrollo]:
        result = await self.db.execute(
            self._base_query(tenant_id).where(
                PlanDesarrollo.administracion_id == administracion_id
            )
        )
        return list(result.scalars().all())


class NodoPlanRepository(BaseRepository[NodoPlan]):
    def __init__(self, db: AsyncSession):
        super().__init__(NodoPlan, db)

    async def get_by_plan(
        self, tenant_id: str | uuid.UUID, plan_id: uuid.UUID
    ) -> Sequence[NodoPlan]:
        result = await self.db.execute(
            self._base_query(tenant_id)
            .where(NodoPlan.plan_id == plan_id)
            .order_by(NodoPlan.orden)
        )
        return list(result.scalars().all())

    async def get_children(
        self, tenant_id: str | uuid.UUID, parent_id: uuid.UUID
    ) -> Sequence[NodoPlan]:
        result = await self.db.execute(
            self._base_query(tenant_id)
            .where(NodoPlan.parent_id == parent_id)
            .order_by(NodoPlan.orden)
        )
        return list(result.scalars().all())

    async def get_tree(
        self, tenant_id: str | uuid.UUID, plan_id: uuid.UUID
    ) -> Sequence[NodoPlan]:
        """Retorna todos los nodos del plan ordenados para construir árbol."""
        result = await self.db.execute(
            self._base_query(tenant_id)
            .where(NodoPlan.plan_id == plan_id)
            .order_by(NodoPlan.orden)
        )
        return list(result.scalars().all())

    async def has_children(self, tenant_id: str | uuid.UUID, node_id: uuid.UUID) -> bool:
        result = await self.db.execute(
            self._base_query(tenant_id).where(NodoPlan.parent_id == node_id).limit(1)
        )
        return result.scalar_one_or_none() is not None


class IndicadorRepository(BaseRepository[Indicador]):
    def __init__(self, db: AsyncSession):
        super().__init__(Indicador, db)

    async def get_by_codigo(
        self, tenant_id: str | uuid.UUID, codigo: str
    ) -> Indicador | None:
        result = await self.db.execute(
            self._base_query(tenant_id).where(Indicador.codigo == codigo)
        )
        return result.scalar_one_or_none()


class MetaRepository(BaseRepository[Meta]):
    def __init__(self, db: AsyncSession):
        super().__init__(Meta, db)

    async def get_by_nodo(
        self, tenant_id: str | uuid.UUID, nodo_plan_id: uuid.UUID
    ) -> Sequence[Meta]:
        result = await self.db.execute(
            self._base_query(tenant_id).where(Meta.nodo_plan_id == nodo_plan_id)
        )
        return list(result.scalars().all())

    async def get_by_codigo(
        self, tenant_id: str | uuid.UUID, codigo: str
    ) -> Meta | None:
        result = await self.db.execute(
            self._base_query(tenant_id).where(Meta.codigo == codigo)
        )
        return result.scalar_one_or_none()

    async def get_with_relations(
        self, tenant_id: str | uuid.UUID, meta_id: uuid.UUID
    ) -> Meta | None:
        result = await self.db.execute(
            self._base_query(tenant_id)
            .where(Meta.id == meta_id)
            .options(
                selectinload(Meta.indicador),
                selectinload(Meta.dependencia),
                selectinload(Meta.nodo_plan),
            )
        )
        return result.scalar_one_or_none()


class ProgramacionAnualRepository(BaseRepository[ProgramacionAnualMeta]):
    def __init__(self, db: AsyncSession):
        super().__init__(ProgramacionAnualMeta, db)

    async def get_by_meta(
        self, tenant_id: str | uuid.UUID, meta_id: uuid.UUID
    ) -> Sequence[ProgramacionAnualMeta]:
        result = await self.db.execute(
            self._base_query(tenant_id)
            .where(ProgramacionAnualMeta.meta_id == meta_id)
            .order_by(ProgramacionAnualMeta.vigencia)
        )
        return list(result.scalars().all())


class AvanceMetaRepository(BaseRepository[AvanceMeta]):
    def __init__(self, db: AsyncSession):
        super().__init__(AvanceMeta, db)

    async def get_by_meta(
        self, tenant_id: str | uuid.UUID, meta_id: uuid.UUID
    ) -> Sequence[AvanceMeta]:
        result = await self.db.execute(
            self._base_query(tenant_id)
            .where(AvanceMeta.meta_id == meta_id)
            .order_by(AvanceMeta.fecha_corte)
        )
        return list(result.scalars().all())
