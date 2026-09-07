from __future__ import annotations

import uuid
from datetime import date
from typing import TYPE_CHECKING

from app.repositories.plan_desarrollo import (
    AvanceMetaRepository,
    IndicadorRepository,
    MetaRepository,
    NodoPlanRepository,
    PlanDesarrolloRepository,
    ProgramacionAnualRepository,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.models.plan_desarrollo import (
        AvanceMeta,
        Indicador,
        Meta,
        NodoPlan,
        PlanDesarrollo,
        ProgramacionAnualMeta,
    )


class PlanDesarrolloService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.plan_repo = PlanDesarrolloRepository(db)
        self.nodo_repo = NodoPlanRepository(db)
        self.indicador_repo = IndicadorRepository(db)
        self.meta_repo = MetaRepository(db)
        self.programacion_repo = ProgramacionAnualRepository(db)
        self.avance_repo = AvanceMetaRepository(db)

    async def create_plan(
        self,
        tenant_id: str,
        administracion_id: str,
        nombre: str,
        vigencia_inicio: int,
        vigencia_fin: int,
        acuerdo_numero: str | None = None,
        fecha_aprobacion: str | None = None,
    ) -> PlanDesarrollo:
        if vigencia_fin < vigencia_inicio:
            raise ValueError("vigencia_fin debe ser >= vigencia_inicio")

        return await self.plan_repo.create(
            tenant_id,
            administracion_id=uuid.UUID(administracion_id),
            nombre=nombre,
            vigencia_inicio=vigencia_inicio,
            vigencia_fin=vigencia_fin,
            acuerdo_numero=acuerdo_numero,
            fecha_aprobacion=date.fromisoformat(fecha_aprobacion) if fecha_aprobacion else None,
            version=1,
            estado="FORMULACION",
        )

    async def update_plan(
        self, tenant_id: str, plan_id: str, **kwargs
    ) -> PlanDesarrollo | None:
        if "fecha_aprobacion" in kwargs and kwargs["fecha_aprobacion"]:
            kwargs["fecha_aprobacion"] = date.fromisoformat(kwargs["fecha_aprobacion"])
        return await self.plan_repo.update(tenant_id, uuid.UUID(plan_id), **kwargs)

    async def get_plan(self, tenant_id: str, plan_id: str) -> PlanDesarrollo | None:
        return await self.plan_repo.get_by_id(tenant_id, uuid.UUID(plan_id))

    async def list_planes(self, tenant_id: str) -> list[PlanDesarrollo]:
        return list(await self.plan_repo.get_multi(tenant_id))

    async def create_nodo(
        self,
        tenant_id: str,
        plan_id: str,
        tipo: str,
        codigo: str,
        nombre: str,
        parent_id: str | None = None,
        orden: int = 0,
    ) -> NodoPlan:
        if parent_id:
            parent = await self.nodo_repo.get_by_id(tenant_id, uuid.UUID(parent_id))
            if parent is None:
                raise ValueError("Nodo padre no encontrado")
            if parent.plan_id != uuid.UUID(plan_id):
                raise ValueError("El nodo padre pertenece a otro plan")

        return await self.nodo_repo.create(
            tenant_id,
            plan_id=uuid.UUID(plan_id),
            parent_id=uuid.UUID(parent_id) if parent_id else None,
            tipo=tipo,
            codigo=codigo,
            nombre=nombre,
            orden=orden,
            estado="ACTIVO",
        )

    async def get_nodos_by_plan(self, tenant_id: str, plan_id: str) -> list[NodoPlan]:
        return list(await self.nodo_repo.get_by_plan(tenant_id, uuid.UUID(plan_id)))

    async def get_nodo_tree(self, tenant_id: str, plan_id: str) -> list[dict]:
        nodos = await self.nodo_repo.get_tree(tenant_id, uuid.UUID(plan_id))
        nodemap = {}
        roots = []
        for n in nodos:
            node_dict = {
                "id": str(n.id),
                "tipo": n.tipo,
                "codigo": n.codigo,
                "nombre": n.nombre,
                "orden": n.orden,
                "estado": n.estado,
                "children": [],
            }
            nodemap[str(n.id)] = node_dict
        for n in nodos:
            node = nodemap[str(n.id)]
            if n.parent_id and str(n.parent_id) in nodemap:
                nodemap[str(n.parent_id)]["children"].append(node)
            else:
                roots.append(node)
        return roots

    async def update_nodo(
        self, tenant_id: str, nodo_id: str, **kwargs
    ) -> NodoPlan | None:
        return await self.nodo_repo.update(tenant_id, uuid.UUID(nodo_id), **kwargs)

    async def delete_nodo(self, tenant_id: str, nodo_id: str) -> bool:
        nodo_uuid = uuid.UUID(nodo_id)
        has_children = await self.nodo_repo.has_children(tenant_id, nodo_uuid)
        if has_children:
            raise ValueError("No se puede eliminar un nodo con hijos")
        return await self.nodo_repo.delete(tenant_id, nodo_uuid)

    async def create_indicador(
        self,
        tenant_id: str,
        codigo: str,
        nombre: str,
        tipo: str,
        unidad_medida: str,
        sentido: str,
        periodicidad: str,
        **kwargs,
    ) -> Indicador:
        existing = await self.indicador_repo.get_by_codigo(tenant_id, codigo)
        if existing:
            raise ValueError(f"Ya existe un indicador con código {codigo}")

        return await self.indicador_repo.create(
            tenant_id,
            codigo=codigo,
            nombre=nombre,
            tipo=tipo,
            unidad_medida=unidad_medida,
            sentido=sentido,
            periodicidad=periodicidad,
            **kwargs,
        )

    async def get_indicador(self, tenant_id: str, indicador_id: str) -> Indicador | None:
        return await self.indicador_repo.get_by_id(tenant_id, uuid.UUID(indicador_id))

    async def list_indicadores(self, tenant_id: str) -> list[Indicador]:
        return list(await self.indicador_repo.get_multi(tenant_id))

    async def update_indicador(
        self, tenant_id: str, indicador_id: str, **kwargs
    ) -> Indicador | None:
        return await self.indicador_repo.update(tenant_id, uuid.UUID(indicador_id), **kwargs)

    async def create_meta(
        self,
        tenant_id: str,
        nodo_plan_id: str,
        indicador_id: str,
        dependencia_id: str,
        codigo: str,
        descripcion: str,
        meta_cuatrienio: int,
        unidad_medida: str,
        linea_base: int | None = None,
        ponderacion: int | None = None,
    ) -> Meta:
        existing = await self.meta_repo.get_by_codigo(tenant_id, codigo)
        if existing:
            raise ValueError(f"Ya existe una meta con código {codigo}")

        nodo = await self.nodo_repo.get_by_id(tenant_id, uuid.UUID(nodo_plan_id))
        if nodo is None:
            raise ValueError("Nodo del plan no encontrado")

        indicador = await self.indicador_repo.get_by_id(tenant_id, uuid.UUID(indicador_id))
        if indicador is None:
            raise ValueError("Indicador no encontrado")

        return await self.meta_repo.create(
            tenant_id,
            nodo_plan_id=uuid.UUID(nodo_plan_id),
            indicador_id=uuid.UUID(indicador_id),
            dependencia_id=uuid.UUID(dependencia_id),
            codigo=codigo,
            descripcion=descripcion,
            meta_cuatrienio=meta_cuatrienio,
            unidad_medida=unidad_medida,
            linea_base=linea_base,
            ponderacion=ponderacion,
            estado="ACTIVA",
        )

    async def get_meta(self, tenant_id: str, meta_id: str) -> Meta | None:
        return await self.meta_repo.get_with_relations(tenant_id, uuid.UUID(meta_id))

    async def list_metas_by_nodo(self, tenant_id: str, nodo_plan_id: str) -> list[Meta]:
        return list(await self.meta_repo.get_by_nodo(tenant_id, uuid.UUID(nodo_plan_id)))

    async def update_meta(self, tenant_id: str, meta_id: str, **kwargs) -> Meta | None:
        return await self.meta_repo.update(tenant_id, uuid.UUID(meta_id), **kwargs)

    async def create_programacion(
        self,
        tenant_id: str,
        meta_id: str,
        vigencia: int,
        valor_programado: int,
        presupuesto_programado: int | None = None,
        observacion: str | None = None,
    ) -> ProgramacionAnualMeta:
        existing = await self.programacion_repo.get_by_meta(tenant_id, uuid.UUID(meta_id))
        for p in existing:
            if p.vigencia == vigencia:
                raise ValueError(f"Ya existe programación para vigencia {vigencia}")

        return await self.programacion_repo.create(
            tenant_id,
            meta_id=uuid.UUID(meta_id),
            vigencia=vigencia,
            valor_programado=valor_programado,
            presupuesto_programado=presupuesto_programado,
            observacion=observacion,
        )

    async def get_programacion_by_meta(
        self, tenant_id: str, meta_id: str
    ) -> list[ProgramacionAnualMeta]:
        return list(await self.programacion_repo.get_by_meta(tenant_id, uuid.UUID(meta_id)))

    async def create_avance(
        self,
        tenant_id: str,
        meta_id: str,
        vigencia: int,
        periodo_tipo: str,
        periodo_numero: int,
        fecha_corte: str,
        valor_periodo: int,
        valor_acumulado: int,
        observacion: str | None = None,
    ) -> AvanceMeta:
        existing = await self.avance_repo.get_by_meta(tenant_id, uuid.UUID(meta_id))
        for a in existing:
            if a.fecha_corte == date.fromisoformat(fecha_corte):
                raise ValueError(f"Ya existe avance para fecha de corte {fecha_corte}")

        meta = await self.meta_repo.get_by_id(tenant_id, uuid.UUID(meta_id))
        if meta is None:
            raise ValueError("Meta no encontrada")

        porcentaje_avance = None
        if meta.meta_cuatrienio > 0:
            porcentaje_avance = int((valor_acumulado / meta.meta_cuatrienio) * 100)

        return await self.avance_repo.create(
            tenant_id,
            meta_id=uuid.UUID(meta_id),
            vigencia=vigencia,
            periodo_tipo=periodo_tipo,
            periodo_numero=periodo_numero,
            fecha_corte=date.fromisoformat(fecha_corte),
            valor_periodo=valor_periodo,
            valor_acumulado=valor_acumulado,
            porcentaje_avance=porcentaje_avance,
            estado_revision="BORRADOR",
            observacion=observacion,
        )

    async def get_avance(self, tenant_id: str, avance_id: str) -> AvanceMeta | None:
        return await self.avance_repo.get_by_id(tenant_id, uuid.UUID(avance_id))

    async def get_avances_by_meta(self, tenant_id: str, meta_id: str) -> list[AvanceMeta]:
        return list(await self.avance_repo.get_by_meta(tenant_id, uuid.UUID(meta_id)))

    async def update_avance(
        self, tenant_id: str, avance_id: str, **kwargs
    ) -> AvanceMeta | None:
        if "fecha_corte" in kwargs and kwargs["fecha_corte"]:
            kwargs["fecha_corte"] = date.fromisoformat(kwargs["fecha_corte"])

        if "valor_acumulado" in kwargs or "valor_periodo" in kwargs:
            avance = await self.avance_repo.get_by_id(tenant_id, uuid.UUID(avance_id))
            if avance:
                meta = await self.meta_repo.get_by_id(tenant_id, avance.meta_id)
                if meta and meta.meta_cuatrienio > 0:
                    valor_acum = kwargs.get("valor_acumulado", avance.valor_acumulado)
                    kwargs["porcentaje_avance"] = int((valor_acum / meta.meta_cuatrienio) * 100)

        return await self.avance_repo.update(tenant_id, uuid.UUID(avance_id), **kwargs)

    async def delete_avance(self, tenant_id: str, avance_id: str) -> bool:
        return await self.avance_repo.delete(tenant_id, uuid.UUID(avance_id))
