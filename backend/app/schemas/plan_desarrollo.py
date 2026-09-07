from __future__ import annotations

from pydantic import BaseModel


class PlanDesarrolloCreate(BaseModel):
    administracion_id: str
    nombre: str
    acuerdo_numero: str | None = None
    fecha_aprobacion: str | None = None
    vigencia_inicio: int
    vigencia_fin: int


class PlanDesarrolloUpdate(BaseModel):
    nombre: str | None = None
    acuerdo_numero: str | None = None
    fecha_aprobacion: str | None = None
    estado: str | None = None


class PlanDesarrolloResponse(BaseModel):
    id: str
    administracion_id: str
    nombre: str
    acuerdo_numero: str | None = None
    fecha_aprobacion: str | None = None
    vigencia_inicio: int
    vigencia_fin: int
    version: int
    estado: str


class NodoPlanCreate(BaseModel):
    plan_id: str
    parent_id: str | None = None
    tipo: str
    codigo: str
    nombre: str
    orden: int = 0


class NodoPlanUpdate(BaseModel):
    nombre: str | None = None
    orden: int | None = None
    estado: str | None = None


class NodoPlanResponse(BaseModel):
    id: str
    plan_id: str
    parent_id: str | None = None
    tipo: str
    codigo: str
    nombre: str
    orden: int
    estado: str


class NodoPlanTreeResponse(BaseModel):
    id: str
    tipo: str
    codigo: str
    nombre: str
    orden: int
    estado: str
    children: list[NodoPlanTreeResponse] = []


class IndicadorCreate(BaseModel):
    codigo: str
    nombre: str
    descripcion: str | None = None
    tipo: str
    unidad_medida: str
    sentido: str
    formula: str | None = None
    fuente: str | None = None
    periodicidad: str
    responsable_dependencia_id: str | None = None


class IndicadorUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    tipo: str | None = None
    unidad_medida: str | None = None
    sentido: str | None = None
    formula: str | None = None
    fuente: str | None = None
    periodicidad: str | None = None
    responsable_dependencia_id: str | None = None


class IndicadorResponse(BaseModel):
    id: str
    codigo: str
    nombre: str
    descripcion: str | None = None
    tipo: str
    unidad_medida: str
    sentido: str
    formula: str | None = None
    fuente: str | None = None
    periodicidad: str
    responsable_dependencia_id: str | None = None


class MetaCreate(BaseModel):
    nodo_plan_id: str
    indicador_id: str
    dependencia_id: str
    codigo: str
    descripcion: str
    linea_base: int | None = None
    meta_cuatrienio: int
    unidad_medida: str
    ponderacion: int | None = None


class MetaUpdate(BaseModel):
    descripcion: str | None = None
    linea_base: int | None = None
    meta_cuatrienio: int | None = None
    unidad_medida: str | None = None
    ponderacion: int | None = None
    estado: str | None = None


class MetaResponse(BaseModel):
    id: str
    nodo_plan_id: str
    indicador_id: str
    dependencia_id: str
    codigo: str
    descripcion: str
    linea_base: int | None = None
    meta_cuatrienio: int
    unidad_medida: str
    ponderacion: int | None = None
    estado: str


class MetaDetailResponse(MetaResponse):
    indicador: IndicadorResponse | None = None


class ProgramacionAnualCreate(BaseModel):
    meta_id: str
    vigencia: int
    valor_programado: int
    presupuesto_programado: int | None = None
    observacion: str | None = None


class ProgramacionAnualResponse(BaseModel):
    id: str
    meta_id: str
    vigencia: int
    valor_programado: int
    presupuesto_programado: int | None = None
    observacion: str | None = None


class AvanceMetaCreate(BaseModel):
    meta_id: str
    vigencia: int
    periodo_tipo: str
    periodo_numero: int
    fecha_corte: str
    valor_periodo: int
    valor_acumulado: int
    observacion: str | None = None


class AvanceMetaResponse(BaseModel):
    id: str
    meta_id: str
    vigencia: int
    periodo_tipo: str
    periodo_numero: int
    fecha_corte: str
    valor_periodo: int
    valor_acumulado: int
    porcentaje_avance: int | None = None
    estado_revision: str
    observacion: str | None = None
