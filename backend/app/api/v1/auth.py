from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.database import get_db
from app.schemas.auth import (
    AsignarRolRequest,
    LoginRequest,
    RefreshRequest,
    RolCreate,
    RolResponse,
    TokenResponse,
    UserCreate,
    UserResponse,
)
from app.services.auth import AuthService

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.core.deps import CurrentTenantId, CurrentUser

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    result = await service.authenticate(body.email, body.password, body.tenant_slug)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas o tenant inactivo",
        )
    return result


@router.post("/refresh", response_model=TokenResponse)
async def refresh(body: RefreshRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    result = await service.refresh_token(body.refresh_token)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido o expirado",
        )
    return result


@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(
    body: UserCreate,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    try:
        user = await service.create_user(
            tenant_id, body.email, body.password, body.nombre_completo, body.dependencia_id
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return UserResponse(
        id=str(user.id),
        email=user.email,
        nombre_completo=user.nombre_completo,
        estado=user.estado,
        dependencia_id=str(user.dependencia_id) if user.dependencia_id else None,
    )


@router.post("/roles", response_model=RolResponse, status_code=201)
async def create_rol(
    body: RolCreate,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    try:
        rol = await service.create_rol(tenant_id, body.nombre, body.descripcion)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return RolResponse(
        id=str(rol.id),
        nombre=rol.nombre,
        descripcion=rol.descripcion,
        es_sistema=rol.es_sistema,
    )


@router.post("/roles/assign", status_code=201)
async def assign_rol(
    body: AsignarRolRequest,
    tenant_id: CurrentTenantId,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    await service.asignar_rol(tenant_id, body.usuario_id, body.rol_id, str(current_user.id))
    return {"detail": "Rol asignado correctamente"}


@router.get("/users/me")
async def get_current_user_info(current_user: CurrentUser):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "nombre_completo": current_user.nombre_completo,
        "estado": current_user.estado,
        "tenant_id": str(current_user.tenant_id),
    }
