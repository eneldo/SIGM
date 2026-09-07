from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select

from app.core.database import get_db
from app.models.control import AlertaGestion
from app.models.ejecucion import (
    ContratoSeguimiento,
    PlanAccion,
    ProyectoInversion,
)
from app.models.plan_desarrollo import AvanceMeta, Meta
from app.repositories.control import AuditEventRepository
from app.repositories.plan_desarrollo import (
    AvanceMetaRepository,
    MetaRepository,
    ProgramacionAnualRepository,
)
from app.schemas.ejecucion import (
    ActividadPlanAccionCreate,
    ActividadPlanAccionResponse,
    ActividadPlanAccionUpdate,
    AlertaGestionCreate,
    AlertaGestionResponse,
    AuditEventResponse,
    ContratoSeguimientoCreate,
    ContratoSeguimientoResponse,
    ContratoSeguimientoUpdate,
    DashboardResumen,
    EjecucionPresupuestalCreate,
    EjecucionPresupuestalResponse,
    EvidenciaCreate,
    EvidenciaResponse,
    PlanAccionCreate,
    PlanAccionResponse,
    PlanAccionUpdate,
    PresupuestoProyectoCreate,
    PresupuestoProyectoResponse,
    PresupuestoProyectoUpdate,
    ProyectoInversionCreate,
    ProyectoInversionResponse,
    ProyectoInversionUpdate,
    ReporteAvanceMeta,
    SnapshotReporteCreate,
    SnapshotReporteResponse,
)
from app.services.control import AlertaService, EvidenciaService, SnapshotService
from app.services.ejecucion import PlanAccionService, ProyectoInversionService

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.core.deps import CurrentTenantId, CurrentUser

router = APIRouter(prefix="/planeacion", tags=["Fases 5-10"])

# ── Fase 5: Planes de Acción ───────────────────────────────────────────────

@router.post("/planes-accion", response_model=PlanAccionResponse, status_code=201)
async def create_plan_accion(
    body: PlanAccionCreate,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanAccionService(db)
    try:
        plan = await service.create_plan(
            tenant_id, body.dependencia_id, body.vigencia, body.nombre
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return plan


@router.get("/planes-accion", response_model=list[PlanAccionResponse])
async def list_planes_accion(
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    vigencia: int | None = None,
):
    service = PlanAccionService(db)
    if vigencia:
        return await service.list_planes_by_vigencia(tenant_id, vigencia)
    return await service.list_planes_by_dependencia(tenant_id, str(current_user.dependencia_id))


@router.get("/planes-accion/{plan_id}", response_model=PlanAccionResponse)
async def get_plan_accion(
    plan_id: str,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanAccionService(db)
    plan = await service.get_plan(tenant_id, plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan de acción no encontrado")
    return plan


@router.patch("/planes-accion/{plan_id}", response_model=PlanAccionResponse)
async def update_plan_accion(
    plan_id: str,
    body: PlanAccionUpdate,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanAccionService(db)
    plan = await service.update_plan(tenant_id, plan_id, **body.model_dump(exclude_unset=True))
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan de acción no encontrado")
    return plan


@router.post("/actividades", response_model=ActividadPlanAccionResponse, status_code=201)
async def create_actividad(
    body: ActividadPlanAccionCreate,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanAccionService(db)
    try:
        act = await service.create_actividad(
            tenant_id,
            body.plan_accion_id,
            body.meta_id,
            body.responsable_usuario_id,
            body.descripcion,
            body.fecha_inicio,
            body.fecha_fin,
            body.presupuesto_estimado,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return act


@router.get("/planes-accion/{plan_id}/actividades", response_model=list[ActividadPlanAccionResponse])
async def list_actividades_by_plan(
    plan_id: str,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanAccionService(db)
    return await service.list_actividades_by_plan(tenant_id, plan_id)


@router.get("/actividades/{actividad_id}", response_model=ActividadPlanAccionResponse)
async def get_actividad(
    actividad_id: str,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanAccionService(db)
    act = await service.get_actividad(tenant_id, actividad_id)
    if act is None:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    return act


@router.patch("/actividades/{actividad_id}", response_model=ActividadPlanAccionResponse)
async def update_actividad(
    actividad_id: str,
    body: ActividadPlanAccionUpdate,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanAccionService(db)
    try:
        act = await service.update_actividad(
            tenant_id, actividad_id, **body.model_dump(exclude_unset=True)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if act is None:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    return act


@router.delete("/actividades/{actividad_id}", status_code=204)
async def delete_actividad(
    actividad_id: str,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanAccionService(db)
    deleted = await service.delete_actividad(tenant_id, actividad_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")


# ── Fase 6: Proyectos de Inversión ─────────────────────────────────────────

@router.post("/proyectos", response_model=ProyectoInversionResponse, status_code=201)
async def create_proyecto(
    body: ProyectoInversionCreate,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = ProyectoInversionService(db)
    try:
        proj = await service.create_proyecto(
            tenant_id,
            body.codigo_interno,
            body.nombre,
            body.dependencia_id,
            body.vigencia_inicio,
            body.vigencia_fin,
            body.codigo_bpin,
            body.objetivo,
            body.fuente_origen,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return proj


@router.get("/proyectos", response_model=list[ProyectoInversionResponse])
async def list_proyectos(
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    estado: str | None = None,
):
    service = ProyectoInversionService(db)
    if estado:
        return await service.list_proyectos_by_estado(tenant_id, estado)
    return await service.list_proyectos_by_dependencia(tenant_id, str(current_user.dependencia_id))


@router.get("/proyectos/{proyecto_id}", response_model=ProyectoInversionResponse)
async def get_proyecto(
    proyecto_id: str,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = ProyectoInversionService(db)
    proj = await service.get_proyecto(tenant_id, proyecto_id)
    if proj is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return proj


@router.patch("/proyectos/{proyecto_id}", response_model=ProyectoInversionResponse)
async def update_proyecto(
    proyecto_id: str,
    body: ProyectoInversionUpdate,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = ProyectoInversionService(db)
    proj = await service.update_proyecto(tenant_id, proyecto_id, **body.model_dump(exclude_unset=True))
    if proj is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return proj


@router.post("/proyectos/{proyecto_id}/presupuestos", response_model=PresupuestoProyectoResponse, status_code=201)
async def create_presupuesto(
    proyecto_id: str,
    body: PresupuestoProyectoCreate,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = ProyectoInversionService(db)
    try:
        pres = await service.create_presupuesto(
            tenant_id,
            proyecto_id,
            body.vigencia,
            body.fuente,
            body.apropiacion_inicial,
            body.adiciones,
            body.reducciones,
            body.apropiacion_definitiva,
            body.origen_dato,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return pres


@router.get("/proyectos/{proyecto_id}/presupuestos", response_model=list[PresupuestoProyectoResponse])
async def list_presupuestos(
    proyecto_id: str,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = ProyectoInversionService(db)
    return await service.list_presupuestos(tenant_id, proyecto_id)


@router.patch("/presupuestos/{presupuesto_id}", response_model=PresupuestoProyectoResponse)
async def update_presupuesto(
    presupuesto_id: str,
    body: PresupuestoProyectoUpdate,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = ProyectoInversionService(db)
    pres = await service.update_presupuesto(tenant_id, presupuesto_id, **body.model_dump(exclude_unset=True))
    if pres is None:
        raise HTTPException(status_code=404, detail="Presupuesto no encontrado")
    return pres


# ── Fase 8: Ejecución Presupuestal ─────────────────────────────────────────

@router.post(
    "/presupuestos/{presupuesto_id}/ejecuciones",
    response_model=EjecucionPresupuestalResponse,
    status_code=201,
)
async def create_ejecucion(
    presupuesto_id: str,
    body: EjecucionPresupuestalCreate,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = ProyectoInversionService(db)
    try:
        ejec = await service.create_ejecucion(
            tenant_id,
            presupuesto_id,
            body.fecha_corte,
            body.cdp,
            body.rp_compromisos,
            body.obligaciones,
            body.pagos,
            body.origen_dato,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ejec


@router.get("/presupuestos/{presupuesto_id}/ejecuciones", response_model=list[EjecucionPresupuestalResponse])
async def list_ejecuciones(
    presupuesto_id: str,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = ProyectoInversionService(db)
    return await service.list_ejecuciones(tenant_id, presupuesto_id)


# ── Fase 6: Contratos ──────────────────────────────────────────────────────

@router.post("/contratos", response_model=ContratoSeguimientoResponse, status_code=201)
async def create_contrato(
    body: ContratoSeguimientoCreate,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = ProyectoInversionService(db)
    try:
        contrato = await service.create_contrato(
            tenant_id,
            body.proyecto_id,
            body.numero,
            body.objeto,
            body.contratista,
            body.valor_inicial,
            body.valor_actual,
            body.secop_id,
            body.supervisor_usuario_id,
            body.fecha_inicio,
            body.fecha_fin,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return contrato


@router.get("/proyectos/{proyecto_id}/contratos", response_model=list[ContratoSeguimientoResponse])
async def list_contratos(
    proyecto_id: str,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = ProyectoInversionService(db)
    return await service.list_contratos(tenant_id, proyecto_id)


@router.get("/contratos/{contrato_id}", response_model=ContratoSeguimientoResponse)
async def get_contrato(
    contrato_id: str,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = ProyectoInversionService(db)
    contrato = await service.get_contrato(tenant_id, contrato_id)
    if contrato is None:
        raise HTTPException(status_code=404, detail="Contrato no encontrado")
    return contrato


@router.patch("/contratos/{contrato_id}", response_model=ContratoSeguimientoResponse)
async def update_contrato(
    contrato_id: str,
    body: ContratoSeguimientoUpdate,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = ProyectoInversionService(db)
    contrato = await service.update_contrato(
        tenant_id, contrato_id, **body.model_dump(exclude_unset=True)
    )
    if contrato is None:
        raise HTTPException(status_code=404, detail="Contrato no encontrado")
    return contrato


@router.delete("/contratos/{contrato_id}", status_code=204)
async def delete_contrato(
    contrato_id: str,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = ProyectoInversionService(db)
    deleted = await service.delete_contrato(tenant_id, contrato_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Contrato no encontrado")


# ── Fase 10: Evidencias ────────────────────────────────────────────────────

@router.post("/evidencias", response_model=EvidenciaResponse, status_code=201)
async def create_evidencia(
    body: EvidenciaCreate,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = EvidenciaService(db)
    evidencia = await service.create_evidencia(
        tenant_id,
        body.entidad_tipo,
        body.entidad_id,
        body.nombre_archivo,
        body.storage_uri,
        body.mime_type,
        body.tamano_bytes,
        body.sha256,
        body.clasificacion,
    )
    return evidencia


@router.get("/evidencias", response_model=list[EvidenciaResponse])
async def list_evidencias(
    entidad_tipo: str,
    entidad_id: str,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = EvidenciaService(db)
    return await service.list_evidencias_by_entidad(tenant_id, entidad_tipo, entidad_id)


@router.delete("/evidencias/{evidencia_id}", status_code=204)
async def delete_evidencia(
    evidencia_id: str,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = EvidenciaService(db)
    deleted = await service.delete_evidencia(tenant_id, evidencia_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Evidencia no encontrada")


# ── Fase 9: Alertas ────────────────────────────────────────────────────────

@router.post("/alertas", response_model=AlertaGestionResponse, status_code=201)
async def create_alerta(
    body: AlertaGestionCreate,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = AlertaService(db)
    alerta = await service.create_alerta(
        tenant_id,
        body.tipo,
        body.severidad,
        body.entidad_tipo,
        body.entidad_id,
        body.mensaje,
    )
    return alerta


@router.get("/alertas", response_model=list[AlertaGestionResponse])
async def list_alertas(
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    estado: str = "ABIERTA",
):
    service = AlertaService(db)
    return await service.list_alertas_by_estado(tenant_id, estado)


@router.post("/alertas/{alerta_id}/atender", response_model=AlertaGestionResponse)
async def atender_alerta(
    alerta_id: str,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = AlertaService(db)
    alerta = await service.atender_alerta(tenant_id, alerta_id)
    if alerta is None:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    return alerta


@router.post("/alertas/{alerta_id}/cerrar", response_model=AlertaGestionResponse)
async def cerrar_alerta(
    alerta_id: str,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = AlertaService(db)
    alerta = await service.cerrar_alerta(tenant_id, alerta_id)
    if alerta is None:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    return alerta


@router.post("/alertas/evaluar", response_model=list[AlertaGestionResponse])
async def evaluar_desviaciones(
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = AlertaService(db)
    return await service.evaluar_desviaciones(tenant_id)


# ── Fase 10: Snapshots ─────────────────────────────────────────────────────

@router.post("/snapshots", response_model=SnapshotReporteResponse, status_code=201)
async def create_snapshot(
    body: SnapshotReporteCreate,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = SnapshotService(db)
    snap = await service.create_snapshot(
        tenant_id,
        body.tipo,
        body.periodo,
        body.fecha_corte,
        body.payload,
        body.payload_hash,
    )
    return snap


@router.get("/snapshots", response_model=list[SnapshotReporteResponse])
async def list_snapshots(
    tipo: str,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    periodo: str | None = None,
):
    service = SnapshotService(db)
    return await service.list_snapshots_by_tipo(tenant_id, tipo, periodo)


@router.post("/snapshots/{snapshot_id}/aprobar", response_model=SnapshotReporteResponse)
async def aprobar_snapshot(
    snapshot_id: str,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = SnapshotService(db)
    snap = await service.aprobar_snapshot(tenant_id, snapshot_id, str(current_user.id))
    if snap is None:
        raise HTTPException(status_code=404, detail="Snapshot no encontrado")
    return snap


# ── Fase 13: Auditoría ─────────────────────────────────────────────────────

@router.get("/audit", response_model=list[AuditEventResponse])
async def list_audit_events(
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    entidad: str | None = None,
    entidad_id: str | None = None,
):
    repo = AuditEventRepository(db)
    if entidad and entidad_id:
        return list(await repo.get_by_entidad(tenant_id, entidad, uuid.UUID(entidad_id)))
    return []


# ── Fase 11: Dashboard ─────────────────────────────────────────────────────

@router.get("/dashboard", response_model=DashboardResumen)
async def get_dashboard(
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    total_planes = (
        await db.execute(
            select(func.count())
            .select_from(PlanAccion)
            .where(PlanAccion.tenant_id == uuid.UUID(tenant_id))
        )
    ).scalar_one()

    total_metas = (
        await db.execute(
            select(func.count())
            .select_from(Meta)
            .where(Meta.tenant_id == uuid.UUID(tenant_id))
        )
    ).scalar_one()

    total_proyectos = (
        await db.execute(
            select(func.count())
            .select_from(ProyectoInversion)
            .where(ProyectoInversion.tenant_id == uuid.UUID(tenant_id))
        )
    ).scalar_one()

    total_contratos = (
        await db.execute(
            select(func.count())
            .select_from(ContratoSeguimiento)
            .where(ContratoSeguimiento.tenant_id == uuid.UUID(tenant_id))
        )
    ).scalar_one()

    metas_con_avance = (
        await db.execute(
            select(func.count(func.distinct(AvanceMeta.meta_id)))
            .where(AvanceMeta.tenant_id == uuid.UUID(tenant_id))
        )
    ).scalar_one()

    alertas_abiertas = (
        await db.execute(
            select(func.count()).select_from(AlertaGestion).where(
                AlertaGestion.tenant_id == uuid.UUID(tenant_id),
                AlertaGestion.estado == "ABIERTA",
            )
        )
    ).scalar_one()

    return DashboardResumen(
        total_planes=total_planes,
        total_metas=total_metas,
        total_proyectos=total_proyectos,
        total_contratos=total_contratos,
        metas_con_avance=metas_con_avance,
        alertas_abiertas=alertas_abiertas,
    )


# ── Fase 12: Reportes ──────────────────────────────────────────────────────

@router.get("/reportes/avance-metas", response_model=list[ReporteAvanceMeta])
async def reporte_avance_metas(
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    meta_repo = MetaRepository(db)
    avance_repo = AvanceMetaRepository(db)
    prog_repo = ProgramacionAnualRepository(db)

    metas = await meta_repo.get_multi(tenant_id, limit=1000)
    reportes = []

    for meta in metas:
        avances = await avance_repo.get_by_meta(tenant_id, meta.id)
        programacion = await prog_repo.get_by_meta(tenant_id, meta.id)

        valor_avance = max((a.valor_acumulado for a in avances), default=0)
        porcentaje = None
        if meta.meta_cuatrienio > 0:
            porcentaje = int((valor_avance / meta.meta_cuatrienio) * 100)

        reportes.append(ReporteAvanceMeta(
            meta_id=str(meta.id),
            meta_codigo=meta.codigo,
            meta_descripcion=meta.descripcion,
            dependencia_nombre="",
            indicador_nombre="",
            unidad_medida=meta.unidad_medida,
            meta_cuatrienio=meta.meta_cuatrienio,
            valor_avance=valor_avance,
            porcentaje_avance=porcentaje,
            programacion=[{"vigencia": p.vigencia, "valor": p.valor_programado} for p in programacion],
            avances=[{"fecha": str(a.fecha_corte), "acumulado": a.valor_acumulado} for a in avances],
        ))

    return reportes
