from __future__ import annotations

import uuid
from datetime import date
from typing import TYPE_CHECKING

from app.repositories.ejecucion import (
    ActividadPlanAccionRepository,
    ContratoSeguimientoRepository,
    EjecucionPresupuestalRepository,
    PlanAccionRepository,
    PresupuestoProyectoRepository,
    ProyectoInversionRepository,
)
from app.repositories.plan_desarrollo import MetaRepository

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.models.ejecucion import (
        ActividadPlanAccion,
        ContratoSeguimiento,
        EjecucionPresupuestal,
        PlanAccion,
        PresupuestoProyecto,
        ProyectoInversion,
    )


class PlanAccionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.plan_repo = PlanAccionRepository(db)
        self.actividad_repo = ActividadPlanAccionRepository(db)
        self.meta_repo = MetaRepository(db)

    async def create_plan(
        self,
        tenant_id: str,
        dependencia_id: str,
        vigencia: int,
        nombre: str,
    ) -> PlanAccion:
        existing = await self.plan_repo.get_by_dependencia(
            tenant_id, uuid.UUID(dependencia_id), vigencia
        )
        version = max((p.version for p in existing), default=0) + 1

        return await self.plan_repo.create(
            tenant_id,
            dependencia_id=uuid.UUID(dependencia_id),
            vigencia=vigencia,
            nombre=nombre,
            version=version,
            estado="BORRADOR",
        )

    async def get_plan(self, tenant_id: str, plan_id: str) -> PlanAccion | None:
        return await self.plan_repo.get_by_id(tenant_id, uuid.UUID(plan_id))

    async def list_planes_by_dependencia(
        self, tenant_id: str, dependencia_id: str
    ) -> list[PlanAccion]:
        return list(await self.plan_repo.get_by_dependencia(tenant_id, uuid.UUID(dependencia_id)))

    async def list_planes_by_vigencia(self, tenant_id: str, vigencia: int) -> list[PlanAccion]:
        return list(await self.plan_repo.get_by_vigencia(tenant_id, vigencia))

    async def update_plan(self, tenant_id: str, plan_id: str, **kwargs) -> PlanAccion | None:
        return await self.plan_repo.update(tenant_id, uuid.UUID(plan_id), **kwargs)

    async def create_actividad(
        self,
        tenant_id: str,
        plan_accion_id: str,
        meta_id: str,
        responsable_usuario_id: str,
        descripcion: str,
        fecha_inicio: str,
        fecha_fin: str,
        presupuesto_estimado: int | None = None,
    ) -> ActividadPlanAccion:
        fi = date.fromisoformat(fecha_inicio)
        ff = date.fromisoformat(fecha_fin)
        if ff < fi:
            raise ValueError("fecha_fin debe ser >= fecha_inicio")

        return await self.actividad_repo.create(
            tenant_id,
            plan_accion_id=uuid.UUID(plan_accion_id),
            meta_id=uuid.UUID(meta_id),
            responsable_usuario_id=uuid.UUID(responsable_usuario_id),
            descripcion=descripcion,
            fecha_inicio=fi,
            fecha_fin=ff,
            presupuesto_estimado=presupuesto_estimado,
            porcentaje_avance=0,
            estado="PENDIENTE",
        )

    async def get_actividad(self, tenant_id: str, actividad_id: str) -> ActividadPlanAccion | None:
        return await self.actividad_repo.get_by_id(tenant_id, uuid.UUID(actividad_id))

    async def list_actividades_by_plan(
        self, tenant_id: str, plan_accion_id: str
    ) -> list[ActividadPlanAccion]:
        return list(await self.actividad_repo.get_by_plan(tenant_id, uuid.UUID(plan_accion_id)))

    async def update_actividad(
        self, tenant_id: str, actividad_id: str, **kwargs
    ) -> ActividadPlanAccion | None:
        if "fecha_inicio" in kwargs and kwargs["fecha_inicio"]:
            kwargs["fecha_inicio"] = date.fromisoformat(kwargs["fecha_inicio"])
        if "fecha_fin" in kwargs and kwargs["fecha_fin"]:
            kwargs["fecha_fin"] = date.fromisoformat(kwargs["fecha_fin"])
        if "porcentaje_avance" in kwargs:
            av = kwargs["porcentaje_avance"]
            if av < 0 or av > 100:
                raise ValueError("porcentaje_avance debe estar entre 0 y 100")
        return await self.actividad_repo.update(tenant_id, uuid.UUID(actividad_id), **kwargs)

    async def delete_actividad(self, tenant_id: str, actividad_id: str) -> bool:
        return await self.actividad_repo.delete(tenant_id, uuid.UUID(actividad_id))


class ProyectoInversionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.proyecto_repo = ProyectoInversionRepository(db)
        self.presupuesto_repo = PresupuestoProyectoRepository(db)
        self.ejecucion_repo = EjecucionPresupuestalRepository(db)
        self.contrato_repo = ContratoSeguimientoRepository(db)

    async def create_proyecto(
        self,
        tenant_id: str,
        codigo_interno: str,
        nombre: str,
        dependencia_id: str,
        vigencia_inicio: int,
        vigencia_fin: int,
        codigo_bpin: str | None = None,
        objetivo: str | None = None,
        fuente_origen: str | None = None,
    ) -> ProyectoInversion:
        if vigencia_fin < vigencia_inicio:
            raise ValueError("vigencia_fin debe ser >= vigencia_inicio")

        existing = await self.proyecto_repo.get_by_codigo(tenant_id, codigo_interno)
        if existing:
            raise ValueError(f"Ya existe proyecto con código {codigo_interno}")

        return await self.proyecto_repo.create(
            tenant_id,
            codigo_interno=codigo_interno,
            codigo_bpin=codigo_bpin,
            nombre=nombre,
            objetivo=objetivo,
            dependencia_id=uuid.UUID(dependencia_id),
            vigencia_inicio=vigencia_inicio,
            vigencia_fin=vigencia_fin,
            estado="FORMULACION",
            fuente_origen=fuente_origen,
        )

    async def get_proyecto(self, tenant_id: str, proyecto_id: str) -> ProyectoInversion | None:
        return await self.proyecto_repo.get_by_id(tenant_id, uuid.UUID(proyecto_id))

    async def list_proyectos_by_dependencia(
        self, tenant_id: str, dependencia_id: str
    ) -> list[ProyectoInversion]:
        return list(await self.proyecto_repo.get_by_dependencia(tenant_id, uuid.UUID(dependencia_id)))

    async def list_proyectos_by_estado(
        self, tenant_id: str, estado: str
    ) -> list[ProyectoInversion]:
        return list(await self.proyecto_repo.get_by_estado(tenant_id, estado))

    async def update_proyecto(
        self, tenant_id: str, proyecto_id: str, **kwargs
    ) -> ProyectoInversion | None:
        return await self.proyecto_repo.update(tenant_id, uuid.UUID(proyecto_id), **kwargs)

    async def create_presupuesto(
        self,
        tenant_id: str,
        proyecto_id: str,
        vigencia: int,
        fuente: str,
        apropiacion_inicial: int,
        adiciones: int = 0,
        reducciones: int = 0,
        apropiacion_definitiva: int | None = None,
        origen_dato: str = "MANUAL",
    ) -> PresupuestoProyecto:
        if apropiacion_definitiva is None:
            apropiacion_definitiva = apropiacion_inicial + adiciones - reducciones

        return await self.presupuesto_repo.create(
            tenant_id,
            proyecto_id=uuid.UUID(proyecto_id),
            vigencia=vigencia,
            fuente=fuente,
            apropiacion_inicial=apropiacion_inicial,
            adiciones=adiciones,
            reducciones=reducciones,
            apropiacion_definitiva=apropiacion_definitiva,
            origen_dato=origen_dato,
        )

    async def list_presupuestos(
        self, tenant_id: str, proyecto_id: str
    ) -> list[PresupuestoProyecto]:
        return list(await self.presupuesto_repo.get_by_proyecto(tenant_id, uuid.UUID(proyecto_id)))

    async def update_presupuesto(
        self, tenant_id: str, presupuesto_id: str, **kwargs
    ) -> PresupuestoProyecto | None:
        if "adiciones" in kwargs or "reducciones" in kwargs:
            pres = await self.presupuesto_repo.get_by_id(tenant_id, uuid.UUID(presupuesto_id))
            if pres:
                adic = kwargs.get("adiciones", pres.adiciones)
                reduc = kwargs.get("reducciones", pres.reducciones)
                kwargs["apropiacion_definitiva"] = pres.apropiacion_inicial + adic - reduc
        return await self.presupuesto_repo.update(tenant_id, uuid.UUID(presupuesto_id), **kwargs)

    async def create_ejecucion(
        self,
        tenant_id: str,
        presupuesto_id: str,
        fecha_corte: str,
        cdp: int | None = None,
        rp_compromisos: int = 0,
        obligaciones: int = 0,
        pagos: int = 0,
        origen_dato: str = "MANUAL",
    ) -> EjecucionPresupuestal:
        fc = date.fromisoformat(fecha_corte)
        existing = await self.ejecucion_repo.get_by_presupuesto_fecha(
            tenant_id, uuid.UUID(presupuesto_id), fc
        )
        if existing:
            raise ValueError(f"Ya existe ejecución para fecha {fecha_corte}")

        porcentaje = None
        pres = await self.presupuesto_repo.get_by_id(tenant_id, uuid.UUID(presupuesto_id))
        if pres and pres.apropiacion_definitiva > 0:
            porcentaje = int((pagos / pres.apropiacion_definitiva) * 100)

        return await self.ejecucion_repo.create(
            tenant_id,
            presupuesto_id=uuid.UUID(presupuesto_id),
            fecha_corte=fc,
            cdp=cdp,
            rp_compromisos=rp_compromisos,
            obligaciones=obligaciones,
            pagos=pagos,
            porcentaje_ejecucion=porcentaje,
            origen_dato=origen_dato,
        )

    async def list_ejecuciones(
        self, tenant_id: str, presupuesto_id: str
    ) -> list[EjecucionPresupuestal]:
        return list(await self.ejecucion_repo.get_by_presupuesto(tenant_id, uuid.UUID(presupuesto_id)))

    async def create_contrato(
        self,
        tenant_id: str,
        proyecto_id: str,
        numero: str,
        objeto: str,
        contratista: str,
        valor_inicial: int,
        valor_actual: int,
        secop_id: str | None = None,
        supervisor_usuario_id: str | None = None,
        fecha_inicio: str | None = None,
        fecha_fin: str | None = None,
    ) -> ContratoSeguimiento:
        existing = await self.contrato_repo.get_by_numero(tenant_id, numero)
        if existing:
            raise ValueError(f"Ya existe contrato con número {numero}")

        return await self.contrato_repo.create(
            tenant_id,
            proyecto_id=uuid.UUID(proyecto_id),
            numero=numero,
            secop_id=secop_id,
            objeto=objeto,
            contratista=contratista,
            supervisor_usuario_id=uuid.UUID(supervisor_usuario_id) if supervisor_usuario_id else None,
            fecha_inicio=date.fromisoformat(fecha_inicio) if fecha_inicio else None,
            fecha_fin=date.fromisoformat(fecha_fin) if fecha_fin else None,
            valor_inicial=valor_inicial,
            valor_actual=valor_actual,
            estado="PLANEADO",
        )

    async def get_contrato(self, tenant_id: str, contrato_id: str) -> ContratoSeguimiento | None:
        return await self.contrato_repo.get_by_id(tenant_id, uuid.UUID(contrato_id))

    async def list_contratos(
        self, tenant_id: str, proyecto_id: str
    ) -> list[ContratoSeguimiento]:
        return list(await self.contrato_repo.get_by_proyecto(tenant_id, uuid.UUID(proyecto_id)))

    async def update_contrato(
        self, tenant_id: str, contrato_id: str, **kwargs
    ) -> ContratoSeguimiento | None:
        if "fecha_inicio" in kwargs and kwargs["fecha_inicio"]:
            kwargs["fecha_inicio"] = date.fromisoformat(kwargs["fecha_inicio"])
        if "fecha_fin" in kwargs and kwargs["fecha_fin"]:
            kwargs["fecha_fin"] = date.fromisoformat(kwargs["fecha_fin"])
        return await self.contrato_repo.update(tenant_id, uuid.UUID(contrato_id), **kwargs)

    async def delete_contrato(self, tenant_id: str, contrato_id: str) -> bool:
        return await self.contrato_repo.delete(tenant_id, uuid.UUID(contrato_id))
