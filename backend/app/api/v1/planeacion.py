from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.database import get_db
from app.schemas.plan_desarrollo import (
    AvanceMetaCreate,
    AvanceMetaResponse,
    IndicadorCreate,
    IndicadorResponse,
    IndicadorUpdate,
    MetaCreate,
    MetaDetailResponse,
    MetaResponse,
    MetaUpdate,
    NodoPlanCreate,
    NodoPlanResponse,
    NodoPlanTreeResponse,
    NodoPlanUpdate,
    PlanDesarrolloCreate,
    PlanDesarrolloResponse,
    PlanDesarrolloUpdate,
    ProgramacionAnualCreate,
    ProgramacionAnualResponse,
)
from app.services.plan_desarrollo import PlanDesarrolloService

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.core.deps import CurrentTenantId, CurrentUser

router = APIRouter(prefix="/planeacion", tags=["Planeación"])


@router.post("/planes", response_model=PlanDesarrolloResponse, status_code=201)
async def create_plan(
    body: PlanDesarrolloCreate,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanDesarrolloService(db)
    try:
        plan = await service.create_plan(
            tenant_id,
            body.administracion_id,
            body.nombre,
            body.vigencia_inicio,
            body.vigencia_fin,
            body.acuerdo_numero,
            body.fecha_aprobacion,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return plan


@router.get("/planes", response_model=list[PlanDesarrolloResponse])
async def list_planes(
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanDesarrolloService(db)
    return await service.list_planes(tenant_id)


@router.get("/planes/{plan_id}", response_model=PlanDesarrolloResponse)
async def get_plan(
    plan_id: str,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanDesarrolloService(db)
    plan = await service.get_plan(tenant_id, plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    return plan


@router.patch("/planes/{plan_id}", response_model=PlanDesarrolloResponse)
async def update_plan(
    plan_id: str,
    body: PlanDesarrolloUpdate,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanDesarrolloService(db)
    plan = await service.update_plan(tenant_id, plan_id, **body.model_dump(exclude_unset=True))
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    return plan


@router.post("/nodos", response_model=NodoPlanResponse, status_code=201)
async def create_nodo(
    body: NodoPlanCreate,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanDesarrolloService(db)
    try:
        nodo = await service.create_nodo(
            tenant_id,
            body.plan_id,
            body.tipo,
            body.codigo,
            body.nombre,
            body.parent_id,
            body.orden,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return nodo


@router.get("/planes/{plan_id}/nodos", response_model=list[NodoPlanResponse])
async def list_nodos_by_plan(
    plan_id: str,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanDesarrolloService(db)
    return await service.get_nodos_by_plan(tenant_id, plan_id)


@router.get("/planes/{plan_id}/arbol", response_model=list[NodoPlanTreeResponse])
async def get_nodo_tree(
    plan_id: str,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanDesarrolloService(db)
    return await service.get_nodo_tree(tenant_id, plan_id)


@router.patch("/nodos/{nodo_id}", response_model=NodoPlanResponse)
async def update_nodo(
    nodo_id: str,
    body: NodoPlanUpdate,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanDesarrolloService(db)
    nodo = await service.update_nodo(tenant_id, nodo_id, **body.model_dump(exclude_unset=True))
    if nodo is None:
        raise HTTPException(status_code=404, detail="Nodo no encontrado")
    return nodo


@router.delete("/nodos/{nodo_id}", status_code=204)
async def delete_nodo(
    nodo_id: str,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanDesarrolloService(db)
    try:
        deleted = await service.delete_nodo(tenant_id, nodo_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not deleted:
        raise HTTPException(status_code=404, detail="Nodo no encontrado")


@router.post("/indicadores", response_model=IndicadorResponse, status_code=201)
async def create_indicador(
    body: IndicadorCreate,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanDesarrolloService(db)
    try:
        indicador = await service.create_indicador(
            tenant_id,
            body.codigo,
            body.nombre,
            body.tipo,
            body.unidad_medida,
            body.sentido,
            body.periodicidad,
            descripcion=body.descripcion,
            formula=body.formula,
            fuente=body.fuente,
            responsable_dependencia_id=body.responsable_dependencia_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return indicador


@router.get("/indicadores", response_model=list[IndicadorResponse])
async def list_indicadores(
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanDesarrolloService(db)
    return await service.list_indicadores(tenant_id)


@router.get("/indicadores/{indicador_id}", response_model=IndicadorResponse)
async def get_indicador(
    indicador_id: str,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanDesarrolloService(db)
    indicador = await service.get_indicador(tenant_id, indicador_id)
    if indicador is None:
        raise HTTPException(status_code=404, detail="Indicador no encontrado")
    return indicador


@router.patch("/indicadores/{indicador_id}", response_model=IndicadorResponse)
async def update_indicador(
    indicador_id: str,
    body: IndicadorUpdate,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanDesarrolloService(db)
    indicador = await service.update_indicador(
        tenant_id, indicador_id, **body.model_dump(exclude_unset=True)
    )
    if indicador is None:
        raise HTTPException(status_code=404, detail="Indicador no encontrado")
    return indicador


@router.post("/metas", response_model=MetaResponse, status_code=201)
async def create_meta(
    body: MetaCreate,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanDesarrolloService(db)
    try:
        meta = await service.create_meta(
            tenant_id,
            body.nodo_plan_id,
            body.indicador_id,
            body.dependencia_id,
            body.codigo,
            body.descripcion,
            body.meta_cuatrienio,
            body.unidad_medida,
            body.linea_base,
            body.ponderacion,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return meta


@router.get("/nodos/{nodo_id}/metas", response_model=list[MetaResponse])
async def list_metas_by_nodo(
    nodo_id: str,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanDesarrolloService(db)
    return await service.list_metas_by_nodo(tenant_id, nodo_id)


@router.get("/metas/{meta_id}", response_model=MetaDetailResponse)
async def get_meta(
    meta_id: str,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanDesarrolloService(db)
    meta = await service.get_meta(tenant_id, meta_id)
    if meta is None:
        raise HTTPException(status_code=404, detail="Meta no encontrada")
    return meta


@router.patch("/metas/{meta_id}", response_model=MetaResponse)
async def update_meta(
    meta_id: str,
    body: MetaUpdate,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanDesarrolloService(db)
    meta = await service.update_meta(tenant_id, meta_id, **body.model_dump(exclude_unset=True))
    if meta is None:
        raise HTTPException(status_code=404, detail="Meta no encontrada")
    return meta


@router.post("/metas/{meta_id}/programacion", response_model=ProgramacionAnualResponse, status_code=201)
async def create_programacion(
    meta_id: str,
    body: ProgramacionAnualCreate,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanDesarrolloService(db)
    try:
        prog = await service.create_programacion(
            tenant_id,
            meta_id,
            body.vigencia,
            body.valor_programado,
            body.presupuesto_programado,
            body.observacion,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return prog


@router.get("/metas/{meta_id}/programacion", response_model=list[ProgramacionAnualResponse])
async def list_programacion_by_meta(
    meta_id: str,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanDesarrolloService(db)
    return await service.get_programacion_by_meta(tenant_id, meta_id)


@router.post("/metas/{meta_id}/avances", response_model=AvanceMetaResponse, status_code=201)
async def create_avance(
    meta_id: str,
    body: AvanceMetaCreate,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanDesarrolloService(db)
    try:
        avance = await service.create_avance(
            tenant_id,
            meta_id,
            body.vigencia,
            body.periodo_tipo,
            body.periodo_numero,
            body.fecha_corte,
            body.valor_periodo,
            body.valor_acumulado,
            body.observacion,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return avance


@router.get("/metas/{meta_id}/avances", response_model=list[AvanceMetaResponse])
async def list_avances_by_meta(
    meta_id: str,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanDesarrolloService(db)
    return await service.get_avances_by_meta(tenant_id, meta_id)


@router.get("/avances/{avance_id}", response_model=AvanceMetaResponse)
async def get_avance(
    avance_id: str,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanDesarrolloService(db)
    avance = await service.get_avance(tenant_id, avance_id)
    if avance is None:
        raise HTTPException(status_code=404, detail="Avance no encontrado")
    return avance


@router.patch("/avances/{avance_id}", response_model=AvanceMetaResponse)
async def update_avance(
    avance_id: str,
    body: AvanceMetaCreate,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanDesarrolloService(db)
    avance = await service.update_avance(tenant_id, avance_id, **body.model_dump(exclude_unset=True))
    if avance is None:
        raise HTTPException(status_code=404, detail="Avance no encontrado")
    return avance


@router.delete("/avances/{avance_id}", status_code=204)
async def delete_avance(
    avance_id: str,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = PlanDesarrolloService(db)
    deleted = await service.delete_avance(tenant_id, avance_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Avance no encontrado")
