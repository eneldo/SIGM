from __future__ import annotations

import uuid
from datetime import date
from typing import TYPE_CHECKING, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.database import get_db
from app.core.deps import CurrentTenantId, CurrentUser
from app.repositories.reporting import ReportingRepository
from app.schemas.reporting import DashboardAlcaldeResponse, MetaTrazabilidadResponse
from app.schemas.reporting import ReporteDTO

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["Reportes gerenciales"])


@router.get("/dashboard/alcalde", response_model=DashboardAlcaldeResponse)
async def dashboard_alcalde(
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    fecha_corte: date | None = Query(default=None),
    formato: str = Query(default="JSON"),
):
    """Dashboard del alcalde con formato de reporte."""
    corte = fecha_corte or date.today()
    report_data = await ReportingRepository(db).get_dashboard(tenant_id, corte)
    return ReporteDTO.export(report_data, formato)


@router.get("/dashboard/dependencias/{id}", response_model=DashboardAlcaldeResponse)
async def dashboard_dependencia(
    id: uuid.UUID,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    fecha_corte: date | None = Query(default=None),
    formato: str = Query(default="JSON"),
):
    """Dashboard de dependencia con formato de reporte."""
    corte = fecha_corte or date.today()
    repository = ReportingRepository(db)
    dependencia = await repository.get_dependencia_dashboard(tenant_id, id, corte)
    if dependencia is None:
        raise HTTPException(status_code=404, detail="Dependencia no encontrada")
    report_data = {"dependencia": dependencia, "fecha_corte": corte}
    return ReporteDTO.export(report_data, formato)


@router.get("/metas/{id}/trazabilidad", response_model=MetaTrazabilidadResponse)
async def trazabilidad_meta(
    id: uuid.UUID,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    fecha_corte: date | None = Query(default=None),
    formato: str = Query(default="JSON"),
):
    """Trazabilidad de meta con formato de reporte."""
    corte = fecha_corte or date.today()
    traceability = await ReportingRepository(db).get_meta_traceability(tenant_id, id, corte)
    if traceability is None:
        raise HTTPException(status_code=404, detail="Meta no encontrada")
    report_data = traceability
    return ReporteDTO.export(report_data, formato)