from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from app.repositories.control import (
    AlertaGestionRepository,
    EvidenciaRepository,
    SnapshotReporteRepository,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.models.control import AlertaGestion, Evidencia, SnapshotReporte


class EvidenciaService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = EvidenciaRepository(db)

    async def create_evidencia(
        self,
        tenant_id: str,
        entidad_tipo: str,
        entidad_id: str,
        nombre_archivo: str,
        storage_uri: str,
        mime_type: str,
        tamano_bytes: int,
        sha256: str,
        clasificacion: str = "INTERNA",
    ) -> Evidencia:
        existing = await self.repo.get_by_entidad(tenant_id, entidad_tipo, uuid.UUID(entidad_id))
        version = max((e.version for e in existing), default=0) + 1

        return await self.repo.create(
            tenant_id,
            entidad_tipo=entidad_tipo,
            entidad_id=uuid.UUID(entidad_id),
            nombre_archivo=nombre_archivo,
            storage_uri=storage_uri,
            mime_type=mime_type,
            tamano_bytes=tamano_bytes,
            sha256=sha256,
            clasificacion=clasificacion,
            version=version,
        )

    async def get_evidencia(self, tenant_id: str, evidencia_id: str) -> Evidencia | None:
        return await self.repo.get_by_id(tenant_id, uuid.UUID(evidencia_id))

    async def list_evidencias_by_entidad(
        self, tenant_id: str, entidad_tipo: str, entidad_id: str
    ) -> list[Evidencia]:
        return list(await self.repo.get_by_entidad(tenant_id, entidad_tipo, uuid.UUID(entidad_id)))

    async def delete_evidencia(self, tenant_id: str, evidencia_id: str) -> bool:
        return await self.repo.delete(tenant_id, uuid.UUID(evidencia_id))


class AlertaService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = AlertaGestionRepository(db)

    async def create_alerta(
        self,
        tenant_id: str,
        tipo: str,
        severidad: str,
        entidad_tipo: str,
        entidad_id: str,
        mensaje: str,
        regla_version: str | None = None,
    ) -> AlertaGestion:
        return await self.repo.create(
            tenant_id,
            tipo=tipo,
            severidad=severidad,
            entidad_tipo=entidad_tipo,
            entidad_id=uuid.UUID(entidad_id),
            mensaje=mensaje,
            regla_version=regla_version,
        )

    async def get_alerta(self, tenant_id: str, alerta_id: str) -> AlertaGestion | None:
        return await self.repo.get_by_id(tenant_id, uuid.UUID(alerta_id))

    async def list_alertas_abiertas(self, tenant_id: str) -> list[AlertaGestion]:
        return list(await self.repo.get_abiertas(tenant_id))

    async def list_alertas_by_estado(
        self, tenant_id: str, estado: str
    ) -> list[AlertaGestion]:
        return list(await self.repo.get_by_estado(tenant_id, estado))

    async def atender_alerta(self, tenant_id: str, alerta_id: str) -> AlertaGestion | None:
        return await self.repo.update(tenant_id, uuid.UUID(alerta_id), estado="ATENDIDA")

    async def cerrar_alerta(self, tenant_id: str, alerta_id: str) -> AlertaGestion | None:
        return await self.repo.update(tenant_id, uuid.UUID(alerta_id), estado="CERRADA")

    async def evaluar_desviaciones(self, tenant_id: str) -> list[AlertaGestion]:
        from app.repositories.ejecucion import EjecucionPresupuestalRepository
        from app.repositories.plan_desarrollo import AvanceMetaRepository, MetaRepository

        avance_repo = AvanceMetaRepository(self.db)
        meta_repo = MetaRepository(self.db)
        EjecucionPresupuestalRepository(self.db)
        alertas_creadas = []

        metas = await meta_repo.get_multi(tenant_id, limit=1000)
        for meta in metas:
            avances = await avance_repo.get_by_meta(tenant_id, meta.id)
            if not avances:
                continue

            ultimo_avance = max(avances, key=lambda a: a.fecha_corte)
            if meta.meta_cuatrienio > 0:
                porcentaje = (ultimo_avance.valor_acumulado / meta.meta_cuatrienio) * 100
                if porcentaje < 25 and ultimo_avance.vigencia >= 2025:
                    existing = await self.repo.get_by_entidad(tenant_id, "META", meta.id)
                    ya_abierta = any(a.estado == "ABIERTA" for a in existing)
                    if not ya_abierta:
                        alerta = await self.create_alerta(
                            tenant_id,
                            tipo="META_ATRASADA",
                            severidad="MEDIA",
                            entidad_tipo="META",
                            entidad_id=str(meta.id),
                            mensaje=f"Meta {meta.codigo} con {int(porcentaje)}% de avance",
                            regla_version="1.0",
                        )
                        alertas_creadas.append(alerta)

        return alertas_creadas


class SnapshotService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = SnapshotReporteRepository(db)

    async def create_snapshot(
        self,
        tenant_id: str,
        tipo: str,
        periodo: str,
        fecha_corte: str,
        payload: dict,
        payload_hash: str,
    ) -> SnapshotReporte:
        return await self.repo.create(
            tenant_id,
            tipo=tipo,
            periodo=periodo,
            fecha_corte=datetime.fromisoformat(fecha_corte),
            payload=payload,
            payload_hash=payload_hash,
            estado="BORRADOR",
        )

    async def get_snapshot(self, tenant_id: str, snapshot_id: str) -> SnapshotReporte | None:
        return await self.repo.get_by_id(tenant_id, uuid.UUID(snapshot_id))

    async def list_snapshots_by_tipo(
        self, tenant_id: str, tipo: str, periodo: str | None = None
    ) -> list[SnapshotReporte]:
        if periodo:
            return list(await self.repo.get_by_tipo_periodo(tenant_id, tipo, periodo))
        return list(await self.repo.get_aprobados(tenant_id, tipo))

    async def aprobar_snapshot(
        self, tenant_id: str, snapshot_id: str, aprobado_by: str
    ) -> SnapshotReporte | None:
        return await self.repo.update(
            tenant_id,
            uuid.UUID(snapshot_id),
            estado="APROBADO",
            aprobado_by=uuid.UUID(aprobado_by),
            aprobado_at=datetime.now(UTC),
        )

    async def delete_snapshot(self, tenant_id: str, snapshot_id: str) -> bool:
        return await self.repo.delete(tenant_id, uuid.UUID(snapshot_id))
