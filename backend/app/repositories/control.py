from __future__ import annotations

from typing import TYPE_CHECKING

from app.models.control import (
    AlertaGestion,
    AuditEvent,
    Evidencia,
    SnapshotReporte,
)
from app.repositories.base import BaseRepository

if TYPE_CHECKING:
    import uuid
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession


class EvidenciaRepository(BaseRepository[Evidencia]):
    def __init__(self, db: AsyncSession):
        super().__init__(Evidencia, db)

    async def get_by_entidad(
        self, tenant_id: str | uuid.UUID, entidad_tipo: str, entidad_id: uuid.UUID
    ) -> Sequence[Evidencia]:
        result = await self.db.execute(
            self._base_query(tenant_id).where(
                Evidencia.entidad_tipo == entidad_tipo,
                Evidencia.entidad_id == entidad_id,
            )
        )
        return list(result.scalars().all())


class AlertaGestionRepository(BaseRepository[AlertaGestion]):
    def __init__(self, db: AsyncSession):
        super().__init__(AlertaGestion, db)

    async def get_by_entidad(
        self, tenant_id: str | uuid.UUID, entidad_tipo: str, entidad_id: uuid.UUID
    ) -> Sequence[AlertaGestion]:
        result = await self.db.execute(
            self._base_query(tenant_id).where(
                AlertaGestion.entidad_tipo == entidad_tipo,
                AlertaGestion.entidad_id == entidad_id,
            )
        )
        return list(result.scalars().all())

    async def get_by_estado(
        self, tenant_id: str | uuid.UUID, estado: str
    ) -> Sequence[AlertaGestion]:
        result = await self.db.execute(
            self._base_query(tenant_id).where(AlertaGestion.estado == estado)
        )
        return list(result.scalars().all())

    async def get_abiertas(self, tenant_id: str | uuid.UUID) -> Sequence[AlertaGestion]:
        return await self.get_by_estado(tenant_id, "ABIERTA")


class SnapshotReporteRepository(BaseRepository[SnapshotReporte]):
    def __init__(self, db: AsyncSession):
        super().__init__(SnapshotReporte, db)

    async def get_by_tipo_periodo(
        self, tenant_id: str | uuid.UUID, tipo: str, periodo: str
    ) -> Sequence[SnapshotReporte]:
        result = await self.db.execute(
            self._base_query(tenant_id).where(
                SnapshotReporte.tipo == tipo,
                SnapshotReporte.periodo == periodo,
            ).order_by(SnapshotReporte.fecha_corte.desc())
        )
        return list(result.scalars().all())

    async def get_aprobados(
        self, tenant_id: str | uuid.UUID, tipo: str
    ) -> Sequence[SnapshotReporte]:
        result = await self.db.execute(
            self._base_query(tenant_id).where(
                SnapshotReporte.tipo == tipo,
                SnapshotReporte.estado == "APROBADO",
            )
        )
        return list(result.scalars().all())


class AuditEventRepository(BaseRepository[AuditEvent]):
    def __init__(self, db: AsyncSession):
        super().__init__(AuditEvent, db)

    async def get_by_entidad(
        self, tenant_id: str | uuid.UUID, entidad: str, entidad_id: uuid.UUID
    ) -> Sequence[AuditEvent]:
        result = await self.db.execute(
            self._base_query(tenant_id).where(
                AuditEvent.entidad == entidad,
                AuditEvent.entidad_id == entidad_id,
            ).order_by(AuditEvent.timestamp.desc())
        )
        return list(result.scalars().all())

    async def get_by_correlation(
        self, tenant_id: str | uuid.UUID, correlation_id: uuid.UUID
    ) -> Sequence[AuditEvent]:
        result = await self.db.execute(
            self._base_query(tenant_id).where(
                AuditEvent.correlation_id == correlation_id
            ).order_by(AuditEvent.timestamp)
        )
        return list(result.scalars().all())

    async def create_event(
        self,
        tenant_id: str | uuid.UUID,
        accion: str,
        entidad: str,
        entidad_id: uuid.UUID | None = None,
        usuario_id: uuid.UUID | None = None,
        ip: str | None = None,
        correlation_id: uuid.UUID | None = None,
        before_data: dict | None = None,
        after_data: dict | None = None,
        metadata_json: dict | None = None,
    ) -> AuditEvent:
        return await self.create(
            tenant_id,
            accion=accion,
            entidad=entidad,
            entidad_id=entidad_id,
            usuario_id=usuario_id,
            ip=ip,
            correlation_id=correlation_id,
            before_data=before_data,
            after_data=after_data,
            metadata_json=metadata_json,
        )
