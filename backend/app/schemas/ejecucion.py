from __future__ import annotations

from pydantic import BaseModel


class PlanAccionCreate(BaseModel):
    dependencia_id: str
    vigencia: int
    nombre: str


class PlanAccionUpdate(BaseModel):
    nombre: str | None = None
    estado: str | None = None


class PlanAccionResponse(BaseModel):
    id: str
    dependencia_id: str
    vigencia: int
    nombre: str
    version: int
    estado: str


class ActividadPlanAccionCreate(BaseModel):
    plan_accion_id: str
    meta_id: str
    responsable_usuario_id: str
    descripcion: str
    fecha_inicio: str
    fecha_fin: str
    presupuesto_estimado: int | None = None


class ActividadPlanAccionUpdate(BaseModel):
    descripcion: str | None = None
    fecha_inicio: str | None = None
    fecha_fin: str | None = None
    presupuesto_estimado: int | None = None
    porcentaje_avance: int | None = None
    estado: str | None = None


class ActividadPlanAccionResponse(BaseModel):
    id: str
    plan_accion_id: str
    meta_id: str
    responsable_usuario_id: str
    descripcion: str
    fecha_inicio: str
    fecha_fin: str
    presupuesto_estimado: int | None = None
    porcentaje_avance: int
    estado: str


class ProyectoInversionCreate(BaseModel):
    codigo_interno: str
    codigo_bpin: str | None = None
    nombre: str
    objetivo: str | None = None
    dependencia_id: str
    vigencia_inicio: int
    vigencia_fin: int
    fuente_origen: str | None = None


class ProyectoInversionUpdate(BaseModel):
    codigo_bpin: str | None = None
    nombre: str | None = None
    objetivo: str | None = None
    vigencia_fin: int | None = None
    estado: str | None = None
    fuente_origen: str | None = None


class ProyectoInversionResponse(BaseModel):
    id: str
    codigo_interno: str
    codigo_bpin: str | None = None
    nombre: str
    objetivo: str | None = None
    dependencia_id: str
    vigencia_inicio: int
    vigencia_fin: int
    estado: str
    fuente_origen: str | None = None


class ProyectoMetaCreate(BaseModel):
    proyecto_id: str
    meta_id: str
    peso_aporte: int | None = None
    observacion: str | None = None


class ProyectoMetaResponse(BaseModel):
    proyecto_id: str
    meta_id: str
    peso_aporte: int | None = None
    observacion: str | None = None


class PresupuestoProyectoCreate(BaseModel):
    proyecto_id: str
    vigencia: int
    fuente: str
    apropiacion_inicial: int
    adiciones: int = 0
    reducciones: int = 0
    apropiacion_definitiva: int
    origen_dato: str = "MANUAL"


class PresupuestoProyectoUpdate(BaseModel):
    adiciones: int | None = None
    reducciones: int | None = None
    apropiacion_definitiva: int | None = None
    origen_dato: str | None = None


class PresupuestoProyectoResponse(BaseModel):
    id: str
    proyecto_id: str
    vigencia: int
    fuente: str
    apropiacion_inicial: int
    adiciones: int
    reducciones: int
    apropiacion_definitiva: int
    origen_dato: str


class EjecucionPresupuestalCreate(BaseModel):
    presupuesto_id: str
    fecha_corte: str
    cdp: int | None = None
    rp_compromisos: int = 0
    obligaciones: int = 0
    pagos: int = 0
    origen_dato: str = "MANUAL"


class EjecucionPresupuestalResponse(BaseModel):
    id: str
    presupuesto_id: str
    fecha_corte: str
    cdp: int | None = None
    rp_compromisos: int
    obligaciones: int
    pagos: int
    porcentaje_ejecucion: int | None = None
    origen_dato: str


class ContratoSeguimientoCreate(BaseModel):
    proyecto_id: str
    numero: str
    secop_id: str | None = None
    objeto: str
    contratista: str
    supervisor_usuario_id: str | None = None
    fecha_inicio: str | None = None
    fecha_fin: str | None = None
    valor_inicial: int
    valor_actual: int


class ContratoSeguimientoUpdate(BaseModel):
    secop_id: str | None = None
    objeto: str | None = None
    contratista: str | None = None
    supervisor_usuario_id: str | None = None
    fecha_inicio: str | None = None
    fecha_fin: str | None = None
    valor_actual: int | None = None
    avance_fisico: int | None = None
    avance_financiero: int | None = None
    estado: str | None = None


class ContratoSeguimientoResponse(BaseModel):
    id: str
    proyecto_id: str
    numero: str
    secop_id: str | None = None
    objeto: str
    contratista: str
    supervisor_usuario_id: str | None = None
    fecha_inicio: str | None = None
    fecha_fin: str | None = None
    valor_inicial: int
    valor_actual: int
    avance_fisico: int | None = None
    avance_financiero: int | None = None
    estado: str


class ContratoMetaCreate(BaseModel):
    contrato_id: str
    meta_id: str
    aporte_estimado: int | None = None
    observacion: str | None = None


class ContratoMetaResponse(BaseModel):
    contrato_id: str
    meta_id: str
    aporte_estimado: int | None = None
    observacion: str | None = None


class EvidenciaCreate(BaseModel):
    entidad_tipo: str
    entidad_id: str
    nombre_archivo: str
    storage_uri: str
    mime_type: str
    tamano_bytes: int
    sha256: str
    clasificacion: str = "INTERNA"


class EvidenciaResponse(BaseModel):
    id: str
    entidad_tipo: str
    entidad_id: str
    nombre_archivo: str
    storage_uri: str
    mime_type: str
    tamano_bytes: int
    sha256: str
    clasificacion: str
    version: int


class AlertaGestionCreate(BaseModel):
    tipo: str
    severidad: str
    entidad_tipo: str
    entidad_id: str
    mensaje: str


class AlertaGestionResponse(BaseModel):
    id: str
    tipo: str
    severidad: str
    entidad_tipo: str
    entidad_id: str
    mensaje: str
    fecha_generacion: str
    estado: str
    regla_version: str | None = None


class SnapshotReporteCreate(BaseModel):
    tipo: str
    periodo: str
    fecha_corte: str
    payload: dict
    payload_hash: str


class SnapshotReporteResponse(BaseModel):
    id: str
    tipo: str
    periodo: str
    fecha_corte: str
    payload_hash: str
    estado: str
    aprobado_by: str | None = None
    aprobado_at: str | None = None


class AuditEventResponse(BaseModel):
    id: str
    usuario_id: str | None = None
    accion: str
    entidad: str
    entidad_id: str | None = None
    timestamp: str
    ip: str | None = None
    correlation_id: str | None = None


class DashboardResumen(BaseModel):
    total_planes: int
    total_metas: int
    total_proyectos: int
    total_contratos: int
    metas_con_avance: int
    alertas_abiertas: int
    avance_global_fisico: int | None = None


class ReporteAvanceMeta(BaseModel):
    meta_id: str
    meta_codigo: str
    meta_descripcion: str
    dependencia_nombre: str
    indicador_nombre: str
    unidad_medida: str
    meta_cuatrienio: int
    valor_avance: int
    porcentaje_avance: int | None = None
    programacion: list[dict]
    avances: list[dict]
