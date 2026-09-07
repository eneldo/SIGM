from __future__ import annotations

from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str
    tenant_slug: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    tenant_id: str
    user_id: str


class RefreshRequest(BaseModel):
    refresh_token: str


class UserCreate(BaseModel):
    email: str
    password: str
    nombre_completo: str
    dependencia_id: str | None = None


class UserResponse(BaseModel):
    id: str
    email: str
    nombre_completo: str
    estado: str
    dependencia_id: str | None = None


class RolCreate(BaseModel):
    nombre: str
    descripcion: str = ""


class RolResponse(BaseModel):
    id: str
    nombre: str
    descripcion: str
    es_sistema: bool


class AsignarRolRequest(BaseModel):
    usuario_id: str
    rol_id: str
