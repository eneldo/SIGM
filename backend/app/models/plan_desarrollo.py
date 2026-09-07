from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TenantModel


class PlanDesarrollo(TenantModel):
    __tablename__ = "planes_desarrollo"

    id: Mapped = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    administracion_id: Mapped = mapped_column(UUID(as_uuid=True), ForeignKey("administraciones.id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(220), nullable=False)
    acuerdo_numero: Mapped[str | None] = mapped_column(String(80), nullable=True)
    fecha_aprobacion: Mapped[date | None] = mapped_column(Date, nullable=True)
    vigencia_inicio: Mapped[int] = mapped_column(Integer, nullable=False)
    vigencia_fin: Mapped[int] = mapped_column(Integer, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    estado: Mapped[str] = mapped_column(String(25), default="FORMULACION", nullable=False)


class NodoPlan(TenantModel):
    __tablename__ = "nodos_plan"

    id: Mapped = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped = mapped_column(UUID(as_uuid=True), ForeignKey("planes_desarrollo.id"), nullable=False)
    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("nodos_plan.id"), nullable=True
    )
    tipo: Mapped[str] = mapped_column(String(40), nullable=False)
    codigo: Mapped[str] = mapped_column(String(80), nullable=False)
    nombre: Mapped[str] = mapped_column(String(300), nullable=False)
    orden: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="ACTIVO", nullable=False)


class Indicador(TenantModel):
    __tablename__ = "indicadores"

    id: Mapped = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo: Mapped[str] = mapped_column(String(80), nullable=False)
    nombre: Mapped[str] = mapped_column(String(250), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    tipo: Mapped[str] = mapped_column(String(30), nullable=False)
    unidad_medida: Mapped[str] = mapped_column(String(60), nullable=False)
    sentido: Mapped[str] = mapped_column(String(20), nullable=False)
    formula: Mapped[str | None] = mapped_column(Text, nullable=True)
    fuente: Mapped[str | None] = mapped_column(String(250), nullable=True)
    periodicidad: Mapped[str] = mapped_column(String(30), nullable=False)
    responsable_dependencia_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("dependencias.id"), nullable=True
    )


class Meta(TenantModel):
    __tablename__ = "metas"

    id: Mapped = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nodo_plan_id: Mapped = mapped_column(UUID(as_uuid=True), ForeignKey("nodos_plan.id"), nullable=False)
    indicador_id: Mapped = mapped_column(UUID(as_uuid=True), ForeignKey("indicadores.id"), nullable=False)
    dependencia_id: Mapped = mapped_column(UUID(as_uuid=True), ForeignKey("dependencias.id"), nullable=False)
    codigo: Mapped[str] = mapped_column(String(80), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    linea_base: Mapped[int | None] = mapped_column(Integer, nullable=True)
    meta_cuatrienio: Mapped[int] = mapped_column(Integer, nullable=False)
    unidad_medida: Mapped[str] = mapped_column(String(60), nullable=False)
    ponderacion: Mapped[int | None] = mapped_column(Integer, nullable=True)
    estado: Mapped[str] = mapped_column(String(20), default="ACTIVA", nullable=False)


class ProgramacionAnualMeta(TenantModel):
    __tablename__ = "programacion_anual_metas"

    id: Mapped = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meta_id: Mapped = mapped_column(UUID(as_uuid=True), ForeignKey("metas.id"), nullable=False)
    vigencia: Mapped[int] = mapped_column(Integer, nullable=False)
    valor_programado: Mapped[int] = mapped_column(Integer, nullable=False)
    presupuesto_programado: Mapped[int | None] = mapped_column(Integer, nullable=True)
    observacion: Mapped[str | None] = mapped_column(Text, nullable=True)


class AvanceMeta(TenantModel):
    __tablename__ = "avances_metas"

    id: Mapped = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meta_id: Mapped = mapped_column(UUID(as_uuid=True), ForeignKey("metas.id"), nullable=False)
    vigencia: Mapped[int] = mapped_column(Integer, nullable=False)
    periodo_tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    periodo_numero: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_corte: Mapped[date] = mapped_column(Date, nullable=False)
    valor_periodo: Mapped[int] = mapped_column(Integer, nullable=False)
    valor_acumulado: Mapped[int] = mapped_column(Integer, nullable=False)
    porcentaje_avance: Mapped[int | None] = mapped_column(Integer, nullable=True)
    estado_revision: Mapped[str] = mapped_column(String(20), default="BORRADOR", nullable=False)
    observacion: Mapped[str | None] = mapped_column(Text, nullable=True)
