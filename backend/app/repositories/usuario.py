from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import select

from app.models.usuario import Rol, Usuario, UsuarioRol
from app.repositories.base import BaseRepository

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class UsuarioRepository(BaseRepository[Usuario]):
    def __init__(self, db: AsyncSession):
        super().__init__(Usuario, db)

    async def get_by_email(self, tenant_id: str | uuid.UUID, email: str) -> Usuario | None:
        result = await self.db.execute(
            self._base_query(tenant_id).where(Usuario.email == email)
        )
        return result.scalar_one_or_none()

    async def get_with_roles(self, tenant_id: str | uuid.UUID, user_id: uuid.UUID) -> Usuario | None:
        result = await self.db.execute(
            self._base_query(tenant_id)
            .where(Usuario.id == user_id)
            .join(UsuarioRol, Usuario.id == UsuarioRol.usuario_id)
            .join(Rol, UsuarioRol.rol_id == Rol.id)
        )
        return result.scalar_one_or_none()


class RolRepository(BaseRepository[Rol]):
    def __init__(self, db: AsyncSession):
        super().__init__(Rol, db)

    async def get_by_name(self, tenant_id: str | uuid.UUID, nombre: str) -> Rol | None:
        result = await self.db.execute(
            self._base_query(tenant_id).where(Rol.nombre == nombre)
        )
        return result.scalar_one_or_none()

    async def get_user_roles(self, tenant_id: str | uuid.UUID, user_id: uuid.UUID) -> list[Rol]:
        result = await self.db.execute(
            select(Rol)
            .join(UsuarioRol, Rol.id == UsuarioRol.rol_id)
            .where(UsuarioRol.usuario_id == user_id)
            .where(Rol.tenant_id == uuid.UUID(tenant_id))
        )
        return list(result.scalars().all())
