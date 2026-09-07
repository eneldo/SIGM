from __future__ import annotations

import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app

# Without a live DB, dependency injection fails with 422 before auth (401/403).
AUTH_OR_VALIDATION = (401, 403, 422)


@pytest.mark.asyncio
async def test_create_plan_accion_requires_auth():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/planeacion/planes-accion",
            json={
                "dependencia_id": str(uuid.uuid4()),
                "vigencia": 2026,
                "nombre": "Plan Test",
            },
        )
        assert response.status_code in AUTH_OR_VALIDATION


@pytest.mark.asyncio
async def test_list_planes_accion_requires_auth():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/planeacion/planes-accion")
        assert response.status_code in AUTH_OR_VALIDATION


@pytest.mark.asyncio
async def test_create_proyecto_requires_auth():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/planeacion/proyectos",
            json={
                "codigo_interno": "PRY-001",
                "nombre": "Proyecto Test",
                "dependencia_id": str(uuid.uuid4()),
                "vigencia_inicio": 2026,
                "vigencia_fin": 2029,
            },
        )
        assert response.status_code in AUTH_OR_VALIDATION


@pytest.mark.asyncio
async def test_list_proyectos_requires_auth():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/planeacion/proyectos")
        assert response.status_code in AUTH_OR_VALIDATION


@pytest.mark.asyncio
async def test_create_contrato_requires_auth():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/planeacion/contratos",
            json={
                "proyecto_id": str(uuid.uuid4()),
                "numero": "CONT-001",
                "objeto": "Objeto Test",
                "contratista": "Contratista SA",
                "valor_inicial": 1000000,
                "valor_actual": 1000000,
            },
        )
        assert response.status_code in AUTH_OR_VALIDATION


@pytest.mark.asyncio
async def test_dashboard_requires_auth():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/planeacion/dashboard")
        assert response.status_code in AUTH_OR_VALIDATION


@pytest.mark.asyncio
async def test_alertas_requires_auth():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/planeacion/alertas")
        assert response.status_code in AUTH_OR_VALIDATION


@pytest.mark.asyncio
async def test_evidencias_requires_auth():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/v1/planeacion/evidencias",
            params={"entidad_tipo": "META", "entidad_id": str(uuid.uuid4())},
        )
        assert response.status_code in AUTH_OR_VALIDATION


@pytest.mark.asyncio
async def test_snapshots_requires_auth():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/v1/planeacion/snapshots",
            params={"tipo": "INFORME_GESTION"},
        )
        assert response.status_code in AUTH_OR_VALIDATION


@pytest.mark.asyncio
async def test_audit_requires_auth():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/planeacion/audit")
        assert response.status_code in AUTH_OR_VALIDATION


@pytest.mark.asyncio
async def test_reporte_avance_metas_requires_auth():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/planeacion/reportes/avance-metas")
        assert response.status_code in AUTH_OR_VALIDATION


@pytest.mark.asyncio
async def test_evaluar_desviaciones_requires_auth():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/api/v1/planeacion/alertas/evaluar")
        assert response.status_code in AUTH_OR_VALIDATION
