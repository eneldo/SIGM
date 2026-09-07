from __future__ import annotations

import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TenantModel


class Municipio(TenantModel):
    __tablename__ = "municipios"

    id: Mapped = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_dane: Mapped[str] = mapped_column(String(5), nullable=False)
    nombre: Mapped[str] = mapped_column(String(160), nullable=False)
    departamento: Mapped[str] = mapped_column(String(120), nullable=False)
    categoria: Mapped[str | None] = mapped_column(String(30), nullable=True)
    nit: Mapped[str | None] = mapped_column(String(30), nullable=True)
    sitio_web: Mapped[str | None] = mapped_column(String(255), nullable=True)
    logo_uri: Mapped[str | None] = mapped_column(String(500), nullable=True)
