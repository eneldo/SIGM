from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TenantModel


class Administracion(TenantModel):
    __tablename__ = "administraciones"

    id: Mapped = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    municipio_id: Mapped = mapped_column(UUID(as_uuid=True), ForeignKey("municipios.id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(180), nullable=False)
    alcalde_nombre: Mapped[str | None] = mapped_column(String(180), nullable=True)
    periodo_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    periodo_fin: Mapped[date] = mapped_column(Date, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="PLANEADA", nullable=False)
