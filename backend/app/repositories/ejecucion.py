from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import selectinload

from app.models.ejecucion import (
    ActividadPlanAccion,
    ContratoSeguimiento,
    EjecucionPresupuestal,
    PlanAccion,
    PresupuestoProyecto,
    ProyectoInversion,
)
from app.repositories.base import BaseRepository

if TYPE_CHECKING:
    import uuid
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession


class PlanAccionRepository(BaseRepository[PlanAccion]):
    def __init__(self, db: AsyncSession):
        super().__init__(PlanAccion, db)

    async def get_by_dependencia(
        self, tenant_id: str | uuid.UUID, dependencia_id: uuid.UUID, vigencia: int | None = None
    ) -> Sequence[PlanAccion]:
        query = self._base_query(tenant_id).where(PlanAccion.dependencia_id == dependencia_id)
        if vigencia is not None:
            query = query.where(PlanAccion.vigencia == vigencia)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_vigencia(
        self, tenant_id: str | uuid.UUID, vigencia: int
    ) -> Sequence[PlanAccion]:
        result = await self.db.execute(
            self._base_query(tenant_id).where(PlanAccion.vigencia == vigencia)
        )
        return list(result.scalars().all())

    async def get_with_actividades(
        self, tenant_id: str | uuid.UUID, plan_id: uuid.UUID
    ) -> PlanAccion | None:
        result = await self.db.execute(
            self._base_query(tenant_id)
            .where(PlanAccion.id == plan_id)
            .options(selectinload(PlanAccion.actividades))
        )
        return result.scalar_one_or_none()


class ActividadPlanAccionRepository(BaseRepository[ActividadPlanAccion]):
    def __init__(self, db: AsyncSession):
        super().__init__(ActividadPlanAccion, db)

    async def get_by_plan(
        self, tenant_id: str | uuid.UUID, plan_accion_id: uuid.UUID
    ) -> Sequence[ActividadPlanAccion]:
        result = await self.db.execute(
            self._base_query(tenant_id).where(
                ActividadPlanAccion.plan_accion_id == plan_accion_id
            )
        )
        return list(result.scalars().all())

    async def get_by_meta(
        self, tenant_id: str | uuid.UUID, meta_id: uuid.UUID
    ) -> Sequence[ActividadPlanAccion]:
        result = await self.db.execute(
            self._base_query(tenant_id).where(ActividadPlanAccion.meta_id == meta_id)
        )
        return list(result.scalars().all())

    async def get_by_responsable(
        self, tenant_id: str | uuid.UUID, responsable_usuario_id: uuid.UUID
    ) -> Sequence[ActividadPlanAccion]:
        result = await self.db.execute(
            self._base_query(tenant_id).where(
                ActividadPlanAccion.responsable_usuario_id == responsable_usuario_id
            )
        )
        return list(result.scalars().all())


class ProyectoInversionRepository(BaseRepository[ProyectoInversion]):
    def __init__(self, db: AsyncSession):
        super().__init__(ProyectoInversion, db)

    async def get_by_codigo(
        self, tenant_id: str | uuid.UUID, codigo_interno: str
    ) -> ProyectoInversion | None:
        result = await self.db.execute(
            self._base_query(tenant_id).where(
                ProyectoInversion.codigo_interno == codigo_interno
            )
        )
        return result.scalar_one_or_none()

    async def get_by_dependencia(
        self, tenant_id: str | uuid.UUID, dependencia_id: uuid.UUID
    ) -> Sequence[ProyectoInversion]:
        result = await self.db.execute(
            self._base_query(tenant_id).where(
                ProyectoInversion.dependencia_id == dependencia_id
            )
        )
        return list(result.scalars().all())

    async def get_by_estado(
        self, tenant_id: str | uuid.UUID, estado: str
    ) -> Sequence[ProyectoInversion]:
        result = await self.db.execute(
            self._base_query(tenant_id).where(ProyectoInversion.estado == estado)
        )
        return list(result.scalars().all())

    async def get_with_metas(
        self, tenant_id: str | uuid.UUID, proyecto_id: uuid.UUID
    ) -> ProyectoInversion | None:
        result = await self.db.execute(
            self._base_query(tenant_id)
            .where(ProyectoInversion.id == proyecto_id)
            .options(selectinload(ProyectoInversion.metas_rel))
        )
        return result.scalar_one_or_none()


class PresupuestoProyectoRepository(BaseRepository[PresupuestoProyecto]):
    def __init__(self, db: AsyncSession):
        super().__init__(PresupuestoProyecto, db)

    async def get_by_proyecto(
        self, tenant_id: str | uuid.UUID, proyecto_id: uuid.UUID
    ) -> Sequence[PresupuestoProyecto]:
        result = await self.db.execute(
            self._base_query(tenant_id).where(
                PresupuestoProyecto.proyecto_id == proyecto_id
            ).order_by(PresupuestoProyecto.vigencia)
        )
        return list(result.scalars().all())

    async def get_by_proyecto_vigencia(
        self, tenant_id: str | uuid.UUID, proyecto_id: uuid.UUID, vigencia: int
    ) -> Sequence[PresupuestoProyecto]:
        result = await self.db.execute(
            self._base_query(tenant_id).where(
                PresupuestoProyecto.proyecto_id == proyecto_id,
                PresupuestoProyecto.vigencia == vigencia,
            )
        )
        return list(result.scalars().all())


class EjecucionPresupuestalRepository(BaseRepository[EjecucionPresupuestal]):
    def __init__(self, db: AsyncSession):
        super().__init__(EjecucionPresupuestal, db)

    async def get_by_presupuesto(
        self, tenant_id: str | uuid.UUID, presupuesto_id: uuid.UUID
    ) -> Sequence[EjecucionPresupuestal]:
        result = await self.db.execute(
            self._base_query(tenant_id)
            .where(EjecucionPresupuestal.presupuesto_id == presupuesto_id)
            .order_by(EjecucionPresupuestal.fecha_corte)
        )
        return list(result.scalars().all())

    async def get_by_presupuesto_fecha(
        self, tenant_id: str | uuid.UUID, presupuesto_id: uuid.UUID, fecha_corte
    ) -> EjecucionPresupuestal | None:
        result = await self.db.execute(
            self._base_query(tenant_id).where(
                EjecucionPresupuestal.presupuesto_id == presupuesto_id,
                EjecucionPresupuestal.fecha_corte == fecha_corte,
            )
        )
        return result.scalar_one_or_none()


class ContratoSeguimientoRepository(BaseRepository[ContratoSeguimiento]):
    def __init__(self, db: AsyncSession):
        super().__init__(ContratoSeguimiento, db)

    async def get_by_proyecto(
        self, tenant_id: str | uuid.UUID, proyecto_id: uuid.UUID
    ) -> Sequence[ContratoSeguimiento]:
        result = await self.db.execute(
            self._base_query(tenant_id).where(
                ContratoSeguimiento.proyecto_id == proyecto_id
            )
        )
        return list(result.scalars().all())

    async def get_by_numero(
        self, tenant_id: str | uuid.UUID, numero: str
    ) -> ContratoSeguimiento | None:
        result = await self.db.execute(
            self._base_query(tenant_id).where(ContratoSeguimiento.numero == numero)
        )
        return result.scalar_one_or_none()
