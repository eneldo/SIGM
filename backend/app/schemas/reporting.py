from __future__ import annotations

import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class _ReportingModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AvanceAgrupado(_ReportingModel):
    id: uuid.UUID
    codigo: str
    nombre: str
    total_metas: int
    metas_con_reporte: int
    avance_porcentaje: float


class TendenciaAnual(_ReportingModel):
    vigencia: int
    valor_programado: int
    valor_avance: int
    avance_porcentaje: float


class DashboardAlcaldeResponse(_ReportingModel):
    fecha_corte: date
    avance_global_pdt: float
    ejecucion_financiera: float
    metas_totales: int
    metas_cumplidas: int
    metas_criticas: int
    metas_sin_reporte: int
    desviaciones_fisico_financieras: int
    proyectos_activos: int
    proyectos_atrasados: int
    contratos: int
    alertas_criticas: int
    avance_por_secretaria: list[AvanceAgrupado]
    avance_por_sector: list[AvanceAgrupado]
    tendencia_cuatrienal: list[TendenciaAnual]


class PlanTrazabilidad(_ReportingModel):
    id: uuid.UUID
    nombre: str
    vigencia_inicio: int
    vigencia_fin: int
    estado: str


class NodoTrazabilidad(_ReportingModel):
    id: uuid.UUID
    parent_id: uuid.UUID | None
    tipo: str
    codigo: str
    nombre: str


class IndicadorTrazabilidad(_ReportingModel):
    id: uuid.UUID
    codigo: str
    nombre: str
    tipo: str
    unidad_medida: str
    sentido: str
    periodicidad: str


class MetaTrazabilidad(_ReportingModel):
    id: uuid.UUID
    codigo: str
    descripcion: str
    dependencia_id: uuid.UUID
    dependencia_nombre: str
    linea_base: int | None
    meta_cuatrienio: int
    unidad_medida: str
    ponderacion: int | None
    estado: str


class ProgramacionTrazabilidad(_ReportingModel):
    id: uuid.UUID
    vigencia: int
    valor_programado: int
    presupuesto_programado: int | None
    observacion: str | None


class AvanceTrazabilidad(_ReportingModel):
    id: uuid.UUID
    vigencia: int
    periodo_tipo: str
    periodo_numero: int
    fecha_corte: date
    valor_periodo: int
    valor_acumulado: int
    porcentaje_avance: int | None
    estado_revision: str
    observacion: str | None


class ProyectoTrazabilidad(_ReportingModel):
    id: uuid.UUID
    codigo_interno: str
    codigo_bpin: str | None
    nombre: str
    dependencia_id: uuid.UUID
    vigencia_inicio: int
    vigencia_fin: int
    estado: str
    peso_aporte: int | None


class PresupuestoTrazabilidad(_ReportingModel):
    id: uuid.UUID
    proyecto_id: uuid.UUID
    vigencia: int
    fuente: str
    apropiacion_inicial: int
    adiciones: int
    reducciones: int
    apropiacion_definitiva: int


class EjecucionTrazabilidad(_ReportingModel):
    id: uuid.UUID
    presupuesto_id: uuid.UUID
    fecha_corte: date
    cdp: int | None
    rp_compromisos: int
    obligaciones: int
    pagos: int
    porcentaje_ejecucion: int | None


class ContratoTrazabilidad(_ReportingModel):
    id: uuid.UUID
    proyecto_id: uuid.UUID
    numero: str
    secop_id: str | None
    objeto: str
    contratista: str
    valor_inicial: int
    valor_actual: int
    avance_fisico: int | None
    avance_financiero: int | None
    estado: str
    aporte_estimado: int | None = None


class EvidenciaTrazabilidad(_ReportingModel):
    id: uuid.UUID
    entidad_tipo: str
    entidad_id: uuid.UUID
    nombre_archivo: str
    storage_uri: str
    mime_type: str
    tamano_bytes: int
    sha256: str
    clasificacion: str
    version: int


class AlertaTrazabilidad(_ReportingModel):
    id: uuid.UUID
    tipo: str
    severidad: str
    entidad_tipo: str
    entidad_id: uuid.UUID
    mensaje: str
    fecha_generacion: datetime
    estado: str


class MetaTrazabilidadResponse(_ReportingModel):
    fecha_corte: date
    meta: MetaTrazabilidad
    plan: PlanTrazabilidad
    nodo: NodoTrazabilidad
    indicador: IndicadorTrazabilidad
    programacion: list[ProgramacionTrazabilidad]
    avances_aprobados: list[AvanceTrazabilidad]
    proyectos: list[ProyectoTrazabilidad]
    presupuestos: list[PresupuestoTrazabilidad]
    ejecuciones: list[EjecucionTrazabilidad]
    contratos: list[ContratoTrazabilidad]
    evidencias: list[EvidenciaTrazabilidad]
    alertas: list[AlertaTrazabilidad]
    limitaciones_modelo: list[str] = Field(default_factory=list)


class ReporteDTO(_ReportingModel):
    """Data Transfer Object for report generation with format support."""
    
    @staticmethod
    def export(data: dict[str, Any], formato: str = "JSON") -> dict[str, Any]:
        """Export data in the specified format.
        
        Currently supports JSON natively; PDF/Excel generation
        can be added in follow-up iterations.
        """
        formato_upper = (formato or "JSON").upper()
        if formato_upper not in {"JSON", "PDF", "EXCEL"}:
            formato_upper = "JSON"
        
        if formato_upper == "PDF":
            # TODO: Implement PDF generation with WeasyPrint or reportlab
            # For now, return data with format marker
            data["_format"] = "pdf"
            data["_note"] = "PDF generation pending - data returned as JSON"
            return data
        elif formato_upper == "EXCEL":
            # TODO: Implement Excel generation with openpyxl
            # For now, return data with format marker
            data["_format"] = "excel"
            data["_note"] = "Excel generation pending - data returned as JSON"
            return data
        else:
            # JSON format (default)
            return data