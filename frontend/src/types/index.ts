export interface User {
  id: string;
  tenant_id: string;
  dependencia_id: string | null;
  nombre_completo: string;
  email: string;
  estado: string;
}

export interface Tenant {
  id: string;
  nombre: string;
  slug: string;
  nit: string;
  estado: string;
}

export interface PlanDesarrollo {
  id: string;
  administracion_id: string;
  nombre: string;
  acuerdo_numero: string | null;
  fecha_aprobacion: string | null;
  vigencia_inicio: number;
  vigencia_fin: number;
  version: number;
  estado: string;
}

export interface NodoPlan {
  id: string;
  plan_id: string;
  parent_id: string | null;
  tipo: string;
  codigo: string;
  nombre: string;
  orden: number;
  estado: string;
}

export interface NodoPlanTree extends NodoPlan {
  children: NodoPlanTree[];
}

export interface Indicador {
  id: string;
  codigo: string;
  nombre: string;
  descripcion: string | null;
  tipo: string;
  unidad_medida: string;
  sentido: string;
  formula: string | null;
  fuente: string | null;
  periodicidad: string;
  responsable_dependencia_id: string | null;
}

export interface Meta {
  id: string;
  nodo_plan_id: string;
  indicador_id: string;
  dependencia_id: string;
  codigo: string;
  descripcion: string;
  linea_base: number | null;
  meta_cuatrienio: number;
  unidad_medida: string;
  ponderacion: number | null;
  estado: string;
}

export interface ProgramacionAnual {
  id: string;
  meta_id: string;
  vigencia: number;
  valor_programado: number;
  presupuesto_programado: number | null;
  observacion: string | null;
}

export interface AvanceMeta {
  id: string;
  meta_id: string;
  vigencia: number;
  periodo_tipo: string;
  periodo_numero: number;
  fecha_corte: string;
  valor_periodo: number;
  valor_acumulado: number;
  porcentaje_avance: number | null;
  estado_revision: string;
  observacion: string | null;
}

export interface PlanAccion {
  id: string;
  dependencia_id: string;
  vigencia: number;
  nombre: string;
  version: number;
  estado: string;
}

export interface ActividadPlanAccion {
  id: string;
  plan_accion_id: string;
  meta_id: string;
  responsable_usuario_id: string;
  descripcion: string;
  fecha_inicio: string;
  fecha_fin: string;
  presupuesto_estimado: number | null;
  porcentaje_avance: number;
  estado: string;
}

export interface ProyectoInversion {
  id: string;
  codigo_interno: string;
  codigo_bpin: string | null;
  nombre: string;
  objetivo: string | null;
  dependencia_id: string;
  vigencia_inicio: number;
  vigencia_fin: number;
  estado: string;
  fuente_origen: string | null;
}

export interface PresupuestoProyecto {
  id: string;
  proyecto_id: string;
  vigencia: number;
  fuente: string;
  apropiacion_inicial: number;
  adiciones: number;
  reducciones: number;
  apropiacion_definitiva: number;
  origen_dato: string;
}

export interface EjecucionPresupuestal {
  id: string;
  presupuesto_id: string;
  fecha_corte: string;
  cdp: number | null;
  rp_compromisos: number;
  obligaciones: number;
  pagos: number;
  porcentaje_ejecucion: number | null;
  origen_dato: string;
}

export interface ContratoSeguimiento {
  id: string;
  proyecto_id: string;
  numero: string;
  secop_id: string | null;
  objeto: string;
  contratista: string;
  supervisor_usuario_id: string | null;
  fecha_inicio: string | null;
  fecha_fin: string | null;
  valor_inicial: number;
  valor_actual: number;
  avance_fisico: number | null;
  avance_financiero: number | null;
  estado: string;
}

export interface Evidencia {
  id: string;
  entidad_tipo: string;
  entidad_id: string;
  nombre_archivo: string;
  storage_uri: string;
  mime_type: string;
  tamano_bytes: number;
  sha256: string;
  clasificacion: string;
  version: number;
}

export interface AlertaGestion {
  id: string;
  tipo: string;
  severidad: string;
  entidad_tipo: string;
  entidad_id: string;
  mensaje: string;
  fecha_generacion: string;
  estado: string;
  regla_version: string | null;
}

export interface SnapshotReporte {
  id: string;
  tipo: string;
  periodo: string;
  fecha_corte: string;
  payload_hash: string;
  estado: string;
  aprobado_by: string | null;
  aprobado_at: string | null;
}

export interface AuditEvent {
  id: string;
  usuario_id: string | null;
  accion: string;
  entidad: string;
  entidad_id: string | null;
  timestamp: string;
  ip: string | null;
  correlation_id: string | null;
}

export interface DashboardResumen {
  total_planes: number;
  total_metas: number;
  total_proyectos: number;
  total_contratos: number;
  metas_con_avance: number;
  alertas_abiertas: number;
  avance_global_fisico: number | null;
}

export interface ReporteAvanceMeta {
  meta_id: string;
  meta_codigo: string;
  meta_descripcion: string;
  dependencia_nombre: string;
  indicador_nombre: string;
  unidad_medida: string;
  meta_cuatrienio: number;
  valor_avance: number;
  porcentaje_avance: number | null;
  programacion: { vigencia: number; valor: number }[];
  avances: { fecha: string; acumulado: number }[];
}
