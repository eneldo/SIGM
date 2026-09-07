from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TenantModel


class PlanAccion(TenantModel):
    __tablename__ = "planes_accion"

    id: Mapped = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dependencia_id: Mapped = mapped_column(UUID(as_uuid=True), ForeignKey("dependencias.id"), nullable=False)
    vigencia: Mapped[int] = mapped_column(Integer, nullable=False)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="BORRADOR", nullable=False)


class ActividadPlanAccion(TenantModel):
    __tablename__ = "actividades_plan_accion"

    id: Mapped = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_accion_id: Mapped = mapped_column(UUID(as_uuid=True), ForeignKey("planes_accion.id"), nullable=False)
    meta_id: Mapped = mapped_column(UUID(as_uuid=True), ForeignKey("metas.id"), nullable=False)
    responsable_usuario_id: Mapped = mapped_column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    fecha_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[date] = mapped_column(Date, nullable=False)
    presupuesto_estimado: Mapped[int | None] = mapped_column(Integer, nullable=True)
    porcentaje_avance: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="PENDIENTE", nullable=False)


class ProyectoInversion(TenantModel):
    __tablename__ = "proyectos_inversion"

    id: Mapped = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_interno: Mapped[str] = mapped_column(String(80), nullable=False)
    codigo_bpin: Mapped[str | None] = mapped_column(String(50), nullable=True)
    nombre: Mapped[str] = mapped_column(String(300), nullable=False)
    objetivo: Mapped[str | None] = mapped_column(Text, nullable=True)
    dependencia_id: Mapped = mapped_column(UUID(as_uuid=True), ForeignKey("dependencias.id"), nullable=False)
    vigencia_inicio: Mapped[int] = mapped_column(Integer, nullable=False)
    vigencia_fin: Mapped[int] = mapped_column(Integer, nullable=False)
    estado: Mapped[str] = mapped_column(String(25), default="FORMULACION", nullable=False)
    fuente_origen: Mapped[str | None] = mapped_column(String(40), nullable=True)


class ProyectoMeta(Base):
    __tablename__ = "proyecto_meta"

    proyecto_id: Mapped = mapped_column(
        UUID(as_uuid=True), ForeignKey("proyectos_inversion.id"), primary_key=True
    )
    meta_id: Mapped = mapped_column(UUID(as_uuid=True), ForeignKey("metas.id"), primary_key=True)
    peso_aporte: Mapped[int | None] = mapped_column(Integer, nullable=True)
    observacion: Mapped[str | None] = mapped_column(Text, nullable=True)


class PresupuestoProyecto(TenantModel):
    __tablename__ = "presupuestos_proyecto"

    id: Mapped = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    proyecto_id: Mapped = mapped_column(UUID(as_uuid=True), ForeignKey("proyectos_inversion.id"), nullable=False)
    vigencia: Mapped[int] = mapped_column(Integer, nullable=False)
    fuente: Mapped[str] = mapped_column(String(120), nullable=False)
    apropiacion_inicial: Mapped[int] = mapped_column(Integer, nullable=False)
    adiciones: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reducciones: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    apropiacion_definitiva: Mapped[int] = mapped_column(Integer, nullable=False)
    origen_dato: Mapped[str] = mapped_column(String(40), default="MANUAL", nullable=False)


class EjecucionPresupuestal(TenantModel):
    __tablename__ = "ejecuciones_presupuestales"

    id: Mapped = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    presupuesto_id: Mapped = mapped_column(UUID(as_uuid=True), ForeignKey("presupuestos_proyecto.id"), nullable=False)
    fecha_corte: Mapped[date] = mapped_column(Date, nullable=False)
    cdp: Mapped[int | None] = mapped_column(Integer, nullable=True)
    rp_compromisos: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    obligaciones: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    pagos: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    porcentaje_ejecucion: Mapped[int | None] = mapped_column(Integer, nullable=True)
    origen_dato: Mapped[str] = mapped_column(String(40), default="MANUAL", nullable=False)


class ContratoSeguimiento(TenantModel):
    __tablename__ = "contratos_seguimiento"

    id: Mapped = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    proyecto_id: Mapped = mapped_column(UUID(as_uuid=True), ForeignKey("proyectos_inversion.id"), nullable=False)
    numero: Mapped[str] = mapped_column(String(100), nullable=False)
    secop_id: Mapped[str | None] = mapped_column(String(150), nullable=True)
    objeto: Mapped[str] = mapped_column(Text, nullable=False)
    contratista: Mapped[str] = mapped_column(String(250), nullable=False)
    supervisor_usuario_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=True
    )
    fecha_inicio: Mapped[date | None] = mapped_column(Date, nullable=True)
    fecha_fin: Mapped[date | None] = mapped_column(Date, nullable=True)
    valor_inicial: Mapped[int] = mapped_column(Integer, nullable=False)
    valor_actual: Mapped[int] = mapped_column(Integer, nullable=False)
    avance_fisico: Mapped[int | None] = mapped_column(Integer, nullable=True)
    avance_financiero: Mapped[int | None] = mapped_column(Integer, nullable=True)
    estado: Mapped[str] = mapped_column(String(25), default="PLANEADO", nullable=False)


class ContratoMeta(Base):
    __tablename__ = "contrato_meta"

    contrato_id: Mapped = mapped_column(
        UUID(as_uuid=True), ForeignKey("contratos_seguimiento.id"), primary_key=True
    )
    meta_id: Mapped = mapped_column(UUID(as_uuid=True), ForeignKey("metas.id"), primary_key=True)
    aporte_estimado: Mapped[int | None] = mapped_column(Integer, nullable=True)
    observacion: Mapped[str | None] = mapped_column(Text, nullable=True)
