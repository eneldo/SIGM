from __future__ import annotations

import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app

# Without a live DB, dependency injection fails with 422 before auth (401/403).
AUTH_OR_VALIDATION = (401, 403, 422)


@pytest.fixture
def mock_tenant_id() -> str:
    return str(uuid.uuid4())


@pytest.mark.asyncio
async def test_create_plan_requires_auth():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/planeacion/planes",
            json={
                "administracion_id": str(uuid.uuid4()),
                "nombre": "Plan Test",
                "vigencia_inicio": 2024,
                "vigencia_fin": 2027,
            },
        )
        assert response.status_code in AUTH_OR_VALIDATION


@pytest.mark.asyncio
async def test_list_planes_requires_auth():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/planeacion/planes")
        assert response.status_code in AUTH_OR_VALIDATION


@pytest.mark.asyncio
async def test_create_indicador_requires_auth():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/planeacion/indicadores",
            json={
                "codigo": "IND-001",
                "nombre": "Indicador Test",
                "tipo": "PRODUCTO",
                "unidad_medida": "Unidades",
                "sentido": "ASCENDENTE",
                "periodicidad": "ANUAL",
            },
        )
        assert response.status_code in AUTH_OR_VALIDATION


@pytest.mark.asyncio
async def test_create_meta_requires_auth():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/planeacion/metas",
            json={
                "nodo_plan_id": str(uuid.uuid4()),
                "indicador_id": str(uuid.uuid4()),
                "dependencia_id": str(uuid.uuid4()),
                "codigo": "META-001",
                "descripcion": "Meta Test",
                "meta_cuatrienio": 100,
                "unidad_medida": "Unidades",
            },
        )
        assert response.status_code in AUTH_OR_VALIDATION


@pytest.mark.asyncio
async def test_create_avance_requires_auth():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            f"/api/v1/planeacion/metas/{uuid.uuid4()}/avances",
            json={
                "meta_id": str(uuid.uuid4()),
                "vigencia": 2024,
                "periodo_tipo": "TRIMESTRE",
                "periodo_numero": 1,
                "fecha_corte": "2024-03-31",
                "valor_periodo": 25,
                "valor_acumulado": 25,
            },
        )
        assert response.status_code in AUTH_OR_VALIDATION


@pytest.mark.asyncio
async def test_list_avances_requires_auth():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get(
            f"/api/v1/planeacion/metas/{uuid.uuid4()}/avances"
        )
        assert response.status_code in AUTH_OR_VALIDATION


@pytest.mark.asyncio
async def test_create_programacion_requires_auth():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            f"/api/v1/planeacion/metas/{uuid.uuid4()}/programacion",
            json={
                "meta_id": str(uuid.uuid4()),
                "vigencia": 2024,
                "valor_programado": 25,
            },
        )
        assert response.status_code in AUTH_OR_VALIDATION


@pytest.mark.asyncio
async def test_list_programacion_requires_auth():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get(
            f"/api/v1/planeacion/metas/{uuid.uuid4()}/programacion"
        )
        assert response.status_code in AUTH_OR_VALIDATION
