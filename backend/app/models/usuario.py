from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TenantModel


class Usuario(TenantModel):
    __tablename__ = "usuarios"

    id: Mapped = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dependencia_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("dependencias.id"), nullable=True
    )
    nombre_completo: Mapped[str] = mapped_column(String(180), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="ACTIVO", nullable=False)
    ultimo_acceso: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Rol(TenantModel):
    __tablename__ = "roles"

    id: Mapped = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(500), default="", nullable=False)
    es_sistema: Mapped[bool] = mapped_column(default=False, nullable=False)


class UsuarioRol(Base):
    __tablename__ = "usuario_roles"

    usuario_id: Mapped = mapped_column(UUID(as_uuid=True), ForeignKey("usuarios.id"), primary_key=True)
    rol_id: Mapped = mapped_column(UUID(as_uuid=True), ForeignKey("roles.id"), primary_key=True)
    asignado_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    asignado_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=True
    )
