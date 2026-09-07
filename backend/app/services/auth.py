from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import select

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.tenant import Tenant
from app.models.usuario import Rol, Usuario, UsuarioRol
from app.repositories.usuario import RolRepository, UsuarioRepository

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.usuario_repo = UsuarioRepository(db)
        self.rol_repo = RolRepository(db)

    async def authenticate(
        self, email: str, password: str, tenant_slug: str
    ) -> dict | None:
        result = await self.db.execute(
            select(Tenant).where(Tenant.slug == tenant_slug)
        )
        tenant = result.scalar_one_or_none()
        if tenant is None or tenant.estado != "ACTIVO":
            return None

        user = await self.usuario_repo.get_by_email(tenant.id, email)
        if user is None:
            return None
        if user.estado != "ACTIVO":
            return None
        if not verify_password(password, user.password_hash):
            return None

        user.ultimo_acceso = datetime.now(UTC)
        await self.db.flush()

        access_token = create_access_token(str(user.id), str(tenant.id))
        refresh_token = create_refresh_token(str(user.id), str(tenant.id))

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "tenant_id": str(tenant.id),
            "user_id": str(user.id),
        }

    async def refresh_token(self, refresh_token: str) -> dict | None:
        payload = decode_token(refresh_token)
        if payload is None or payload.get("type") != "refresh":
            return None

        user_id = payload.get("sub")
        tenant_id = payload.get("tenant_id")

        user = await self.usuario_repo.get_by_id(tenant_id, uuid.UUID(user_id))
        if user is None or user.estado != "ACTIVO":
            return None

        access_token = create_access_token(user_id, tenant_id)
        new_refresh = create_refresh_token(user_id, tenant_id)

        return {
            "access_token": access_token,
            "refresh_token": new_refresh,
            "token_type": "bearer",
            "tenant_id": tenant_id,
            "user_id": user_id,
        }

    async def create_user(
        self,
        tenant_id: str,
        email: str,
        password: str,
        nombre_completo: str,
        dependencia_id: str | None = None,
    ) -> Usuario:
        existing = await self.usuario_repo.get_by_email(tenant_id, email)
        if existing:
            raise ValueError("El email ya está registrado en este tenant")

        return await self.usuario_repo.create(
            tenant_id,
            email=email,
            password_hash=hash_password(password),
            nombre_completo=nombre_completo,
            dependencia_id=uuid.UUID(dependencia_id) if dependencia_id else None,
            estado="ACTIVO",
        )

    async def create_rol(self, tenant_id: str, nombre: str, descripcion: str = "") -> Rol:
        existing = await self.rol_repo.get_by_name(tenant_id, nombre)
        if existing:
            raise ValueError("El rol ya existe en este tenant")

        return await self.rol_repo.create(
            tenant_id, nombre=nombre, descripcion=descripcion, es_sistema=False
        )

    async def asignar_rol(
        self, tenant_id: str, usuario_id: str, rol_id: str, asignado_by: str | None = None
    ) -> UsuarioRol:
        usuario_rol = UsuarioRol(
            usuario_id=uuid.UUID(usuario_id),
            rol_id=uuid.UUID(rol_id),
            asignado_by=uuid.UUID(asignado_by) if asignado_by else None,
        )
        self.db.add(usuario_rol)
        await self.db.flush()
        return usuario_rol

    async def get_user_roles(self, tenant_id: str, user_id: str) -> list[Rol]:
        return await self.rol_repo.get_user_roles(tenant_id, uuid.UUID(user_id))
