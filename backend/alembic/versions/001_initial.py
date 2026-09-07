"""initial schema

Revision ID: 001_initial
Revises: 
Create Date: 2026-09-06

"""
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = '001_initial'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Extensiones
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
    op.execute("CREATE EXTENSION IF NOT EXISTS citext")

    # tenants
    op.create_table(
        'tenants',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('nombre', sa.String(180), nullable=False),
        sa.Column('slug', sa.String(80), unique=True, nullable=False),
        sa.Column('nit', sa.String(30), nullable=False),
        sa.Column('estado', sa.String(20), nullable=False, server_default='ACTIVO'),
        sa.Column('configuracion', postgresql.JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # municipios
    op.create_table(
        'municipios',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False, index=True),
        sa.Column('codigo_dane', sa.String(5), nullable=False),
        sa.Column('nombre', sa.String(160), nullable=False),
        sa.Column('departamento', sa.String(120), nullable=False),
        sa.Column('categoria', sa.String(30), nullable=True),
        sa.Column('nit', sa.String(30), nullable=True),
        sa.Column('sitio_web', sa.String(255), nullable=True),
        sa.Column('logo_uri', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint('tenant_id', 'codigo_dane'),
    )

    # administraciones
    op.create_table(
        'administraciones',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False, index=True),
        sa.Column('municipio_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('municipios.id'), nullable=False),
        sa.Column('nombre', sa.String(180), nullable=False),
        sa.Column('alcalde_nombre', sa.String(180), nullable=True),
        sa.Column('periodo_inicio', sa.Date, nullable=False),
        sa.Column('periodo_fin', sa.Date, nullable=False),
        sa.Column('estado', sa.String(20), nullable=False, server_default='PLANEADA'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # dependencias (antes que usuarios por FK)
    op.create_table(
        'dependencias',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False, index=True),
        sa.Column('parent_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('dependencias.id'), nullable=True),
        sa.Column('codigo', sa.String(40), nullable=False),
        sa.Column('nombre', sa.String(180), nullable=False),
        sa.Column('tipo', sa.String(40), nullable=False),
        sa.Column('responsable_usuario_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('estado', sa.String(20), nullable=False, server_default='ACTIVA'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # usuarios
    op.create_table(
        'usuarios',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False, index=True),
        sa.Column('dependencia_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('dependencias.id'), nullable=True),
        sa.Column('nombre_completo', sa.String(180), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('estado', sa.String(20), nullable=False, server_default='ACTIVO'),
        sa.Column('ultimo_acceso', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint('tenant_id', 'email'),
    )

    # FK dependencias -> usuarios
    op.create_foreign_key('fk_dependencias_responsable', 'dependencias', 'usuarios', ['responsable_usuario_id'], ['id'])

    # roles
    op.create_table(
        'roles',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False, index=True),
        sa.Column('nombre', sa.String(80), nullable=False),
        sa.Column('descripcion', sa.String(500), nullable=False, server_default=''),
        sa.Column('es_sistema', sa.Boolean, nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint('tenant_id', 'nombre'),
    )

    # usuario_roles
    op.create_table(
        'usuario_roles',
        sa.Column('usuario_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('usuarios.id'), primary_key=True),
        sa.Column('rol_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('roles.id'), primary_key=True),
        sa.Column('asignado_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('asignado_by', postgresql.UUID(as_uuid=True), sa.ForeignKey('usuarios.id'), nullable=True),
    )

    # planes_desarrollo
    op.create_table(
        'planes_desarrollo',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False, index=True),
        sa.Column('administracion_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('administraciones.id'), nullable=False),
        sa.Column('nombre', sa.String(220), nullable=False),
        sa.Column('acuerdo_numero', sa.String(80), nullable=True),
        sa.Column('fecha_aprobacion', sa.Date, nullable=True),
        sa.Column('vigencia_inicio', sa.Integer, nullable=False),
        sa.Column('vigencia_fin', sa.Integer, nullable=False),
        sa.Column('version', sa.Integer, nullable=False, server_default='1'),
        sa.Column('estado', sa.String(25), nullable=False, server_default='FORMULACION'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # nodos_plan
    op.create_table(
        'nodos_plan',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False, index=True),
        sa.Column('plan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('planes_desarrollo.id'), nullable=False),
        sa.Column('parent_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('nodos_plan.id'), nullable=True),
        sa.Column('tipo', sa.String(40), nullable=False),
        sa.Column('codigo', sa.String(80), nullable=False),
        sa.Column('nombre', sa.String(300), nullable=False),
        sa.Column('orden', sa.Integer, nullable=False, server_default='0'),
        sa.Column('estado', sa.String(20), nullable=False, server_default='ACTIVO'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint('plan_id', 'codigo'),
    )

    # indicadores
    op.create_table(
        'indicadores',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False, index=True),
        sa.Column('codigo', sa.String(80), nullable=False),
        sa.Column('nombre', sa.String(250), nullable=False),
        sa.Column('descripcion', sa.Text, nullable=True),
        sa.Column('tipo', sa.String(30), nullable=False),
        sa.Column('unidad_medida', sa.String(60), nullable=False),
        sa.Column('sentido', sa.String(20), nullable=False),
        sa.Column('formula', sa.Text, nullable=True),
        sa.Column('fuente', sa.String(250), nullable=True),
        sa.Column('periodicidad', sa.String(30), nullable=False),
        sa.Column('responsable_dependencia_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('dependencias.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint('tenant_id', 'codigo'),
    )

    # metas
    op.create_table(
        'metas',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False, index=True),
        sa.Column('nodo_plan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('nodos_plan.id'), nullable=False),
        sa.Column('indicador_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('indicadores.id'), nullable=False),
        sa.Column('dependencia_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('dependencias.id'), nullable=False),
        sa.Column('codigo', sa.String(80), nullable=False),
        sa.Column('descripcion', sa.Text, nullable=False),
        sa.Column('linea_base', sa.Integer, nullable=True),
        sa.Column('meta_cuatrienio', sa.Integer, nullable=False),
        sa.Column('unidad_medida', sa.String(60), nullable=False),
        sa.Column('ponderacion', sa.Integer, nullable=True),
        sa.Column('estado', sa.String(20), nullable=False, server_default='ACTIVA'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint('tenant_id', 'codigo'),
    )

    # programacion_anual_metas
    op.create_table(
        'programacion_anual_metas',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False, index=True),
        sa.Column('meta_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('metas.id'), nullable=False),
        sa.Column('vigencia', sa.Integer, nullable=False),
        sa.Column('valor_programado', sa.Integer, nullable=False),
        sa.Column('presupuesto_programado', sa.Integer, nullable=True),
        sa.Column('observacion', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint('meta_id', 'vigencia'),
    )

    # avances_metas
    op.create_table(
        'avances_metas',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False, index=True),
        sa.Column('meta_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('metas.id'), nullable=False),
        sa.Column('vigencia', sa.Integer, nullable=False),
        sa.Column('periodo_tipo', sa.String(20), nullable=False),
        sa.Column('periodo_numero', sa.Integer, nullable=False),
        sa.Column('fecha_corte', sa.Date, nullable=False),
        sa.Column('valor_periodo', sa.Integer, nullable=False),
        sa.Column('valor_acumulado', sa.Integer, nullable=False),
        sa.Column('porcentaje_avance', sa.Integer, nullable=True),
        sa.Column('estado_revision', sa.String(20), nullable=False, server_default='BORRADOR'),
        sa.Column('observacion', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint('meta_id', 'fecha_corte'),
    )

    # planes_accion
    op.create_table(
        'planes_accion',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False, index=True),
        sa.Column('dependencia_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('dependencias.id'), nullable=False),
        sa.Column('vigencia', sa.Integer, nullable=False),
        sa.Column('nombre', sa.String(200), nullable=False),
        sa.Column('version', sa.Integer, nullable=False, server_default='1'),
        sa.Column('estado', sa.String(20), nullable=False, server_default='BORRADOR'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint('dependencia_id', 'vigencia', 'version'),
    )

    # actividades_plan_accion
    op.create_table(
        'actividades_plan_accion',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False, index=True),
        sa.Column('plan_accion_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('planes_accion.id'), nullable=False),
        sa.Column('meta_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('metas.id'), nullable=False),
        sa.Column('responsable_usuario_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('usuarios.id'), nullable=False),
        sa.Column('descripcion', sa.Text, nullable=False),
        sa.Column('fecha_inicio', sa.Date, nullable=False),
        sa.Column('fecha_fin', sa.Date, nullable=False),
        sa.Column('presupuesto_estimado', sa.Integer, nullable=True),
        sa.Column('porcentaje_avance', sa.Integer, nullable=False, server_default='0'),
        sa.Column('estado', sa.String(20), nullable=False, server_default='PENDIENTE'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # proyectos_inversion
    op.create_table(
        'proyectos_inversion',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False, index=True),
        sa.Column('codigo_interno', sa.String(80), nullable=False),
        sa.Column('codigo_bpin', sa.String(50), nullable=True),
        sa.Column('nombre', sa.String(300), nullable=False),
        sa.Column('objetivo', sa.Text, nullable=True),
        sa.Column('dependencia_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('dependencias.id'), nullable=False),
        sa.Column('vigencia_inicio', sa.Integer, nullable=False),
        sa.Column('vigencia_fin', sa.Integer, nullable=False),
        sa.Column('estado', sa.String(25), nullable=False, server_default='FORMULACION'),
        sa.Column('fuente_origen', sa.String(40), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint('tenant_id', 'codigo_interno'),
    )

    # proyecto_meta
    op.create_table(
        'proyecto_meta',
        sa.Column('proyecto_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('proyectos_inversion.id'), primary_key=True),
        sa.Column('meta_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('metas.id'), primary_key=True),
        sa.Column('peso_aporte', sa.Integer, nullable=True),
        sa.Column('observacion', sa.Text, nullable=True),
    )

    # presupuestos_proyecto
    op.create_table(
        'presupuestos_proyecto',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False, index=True),
        sa.Column('proyecto_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('proyectos_inversion.id'), nullable=False),
        sa.Column('vigencia', sa.Integer, nullable=False),
        sa.Column('fuente', sa.String(120), nullable=False),
        sa.Column('apropiacion_inicial', sa.Integer, nullable=False),
        sa.Column('adiciones', sa.Integer, nullable=False, server_default='0'),
        sa.Column('reducciones', sa.Integer, nullable=False, server_default='0'),
        sa.Column('apropiacion_definitiva', sa.Integer, nullable=False),
        sa.Column('origen_dato', sa.String(40), nullable=False, server_default='MANUAL'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # ejecuciones_presupuestales
    op.create_table(
        'ejecuciones_presupuestales',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False, index=True),
        sa.Column('presupuesto_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('presupuestos_proyecto.id'), nullable=False),
        sa.Column('fecha_corte', sa.Date, nullable=False),
        sa.Column('cdp', sa.Integer, nullable=True),
        sa.Column('rp_compromisos', sa.Integer, nullable=False, server_default='0'),
        sa.Column('obligaciones', sa.Integer, nullable=False, server_default='0'),
        sa.Column('pagos', sa.Integer, nullable=False, server_default='0'),
        sa.Column('porcentaje_ejecucion', sa.Integer, nullable=True),
        sa.Column('origen_dato', sa.String(40), nullable=False, server_default='MANUAL'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint('presupuesto_id', 'fecha_corte'),
    )

    # contratos_seguimiento
    op.create_table(
        'contratos_seguimiento',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False, index=True),
        sa.Column('proyecto_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('proyectos_inversion.id'), nullable=False),
        sa.Column('numero', sa.String(100), nullable=False),
        sa.Column('secop_id', sa.String(150), nullable=True),
        sa.Column('objeto', sa.Text, nullable=False),
        sa.Column('contratista', sa.String(250), nullable=False),
        sa.Column('supervisor_usuario_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('usuarios.id'), nullable=True),
        sa.Column('fecha_inicio', sa.Date, nullable=True),
        sa.Column('fecha_fin', sa.Date, nullable=True),
        sa.Column('valor_inicial', sa.Integer, nullable=False),
        sa.Column('valor_actual', sa.Integer, nullable=False),
        sa.Column('avance_fisico', sa.Integer, nullable=True),
        sa.Column('avance_financiero', sa.Integer, nullable=True),
        sa.Column('estado', sa.String(25), nullable=False, server_default='PLANEADO'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint('tenant_id', 'numero'),
    )

    # contrato_meta
    op.create_table(
        'contrato_meta',
        sa.Column('contrato_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('contratos_seguimiento.id'), primary_key=True),
        sa.Column('meta_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('metas.id'), primary_key=True),
        sa.Column('aporte_estimado', sa.Integer, nullable=True),
        sa.Column('observacion', sa.Text, nullable=True),
    )

    # evidencias
    op.create_table(
        'evidencias',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False, index=True),
        sa.Column('entidad_tipo', sa.String(50), nullable=False),
        sa.Column('entidad_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('nombre_archivo', sa.String(255), nullable=False),
        sa.Column('storage_uri', sa.String(700), nullable=False),
        sa.Column('mime_type', sa.String(120), nullable=False),
        sa.Column('tamano_bytes', sa.Integer, nullable=False),
        sa.Column('sha256', sa.String(64), nullable=False),
        sa.Column('clasificacion', sa.String(30), nullable=False, server_default='INTERNA'),
        sa.Column('version', sa.Integer, nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # alertas_gestion
    op.create_table(
        'alertas_gestion',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False, index=True),
        sa.Column('tipo', sa.String(60), nullable=False),
        sa.Column('severidad', sa.String(15), nullable=False),
        sa.Column('entidad_tipo', sa.String(50), nullable=False),
        sa.Column('entidad_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('mensaje', sa.Text, nullable=False),
        sa.Column('fecha_generacion', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('estado', sa.String(20), nullable=False, server_default='ABIERTA'),
        sa.Column('regla_version', sa.String(30), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # snapshots_reporte
    op.create_table(
        'snapshots_reporte',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False, index=True),
        sa.Column('tipo', sa.String(40), nullable=False),
        sa.Column('periodo', sa.String(40), nullable=False),
        sa.Column('fecha_corte', sa.DateTime(timezone=True), nullable=False),
        sa.Column('payload', postgresql.JSONB, nullable=False),
        sa.Column('payload_hash', sa.String(64), nullable=False),
        sa.Column('estado', sa.String(20), nullable=False, server_default='BORRADOR'),
        sa.Column('aprobado_by', postgresql.UUID(as_uuid=True), sa.ForeignKey('usuarios.id'), nullable=True),
        sa.Column('aprobado_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # audit_events
    op.create_table(
        'audit_events',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False, index=True),
        sa.Column('usuario_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('usuarios.id'), nullable=True),
        sa.Column('accion', sa.String(50), nullable=False),
        sa.Column('entidad', sa.String(80), nullable=False),
        sa.Column('entidad_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('ip', sa.String(45), nullable=True),
        sa.Column('correlation_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('before_data', postgresql.JSONB, nullable=True),
        sa.Column('after_data', postgresql.JSONB, nullable=True),
        sa.Column('metadata', postgresql.JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # Índices adicionales
    op.create_index('ix_municipios_codigo_dane', 'municipios', ['codigo_dane'])
    op.create_index('ix_dependencias_parent', 'dependencias', ['parent_id'])
    op.create_index('ix_dependencias_estado', 'dependencias', ['estado'])
    op.create_index('ix_usuarios_email', 'usuarios', ['email'])
    op.create_index('ix_usuarios_dependencia', 'usuarios', ['dependencia_id'])
    op.create_index('ix_planes_desarrollo_estado', 'planes_desarrollo', ['estado'])
    op.create_index('ix_nodos_plan_parent', 'nodos_plan', ['parent_id'])
    op.create_index('ix_nodos_plan_tipo', 'nodos_plan', ['tipo'])
    op.create_index('ix_indicadores_tipo', 'indicadores', ['tipo'])
    op.create_index('ix_metas_nodo', 'metas', ['nodo_plan_id'])
    op.create_index('ix_metas_dependencia', 'metas', ['dependencia_id'])
    op.create_index('ix_metas_indicador', 'metas', ['indicador_id'])
    op.create_index('ix_avances_meta_fecha', 'avances_metas', ['meta_id', 'fecha_corte'])
    op.create_index('ix_avances_tenant_vigencia', 'avances_metas', ['tenant_id', 'vigencia'])
    op.create_index('ix_proyectos_estado', 'proyectos_inversion', ['estado'])
    op.create_index('ix_proyectos_dependencia', 'proyectos_inversion', ['dependencia_id'])
    op.create_index('ix_proyectos_bpin', 'proyectos_inversion', ['codigo_bpin'])
    op.create_index('ix_presupuestos_proyecto_vigencia', 'presupuestos_proyecto', ['proyecto_id', 'vigencia'])
    op.create_index('ix_ejecuciones_fecha', 'ejecuciones_presupuestales', ['presupuesto_id', 'fecha_corte'])
    op.create_index('ix_contratos_proyecto', 'contratos_seguimiento', ['proyecto_id'])
    op.create_index('ix_contratos_estado', 'contratos_seguimiento', ['estado'])
    op.create_index('ix_evidencias_entidad', 'evidencias', ['tenant_id', 'entidad_tipo', 'entidad_id'])
    op.create_index('ix_evidencias_sha256', 'evidencias', ['sha256'])
    op.create_index('ix_alertas_estado_severidad', 'alertas_gestion', ['tenant_id', 'estado', 'severidad'])
    op.create_index('ix_alertas_entidad', 'alertas_gestion', ['entidad_tipo', 'entidad_id'])
    op.create_index('ix_snapshots_tipo_periodo', 'snapshots_reporte', ['tenant_id', 'tipo', 'periodo'])
    op.create_index('ix_audit_tenant_timestamp', 'audit_events', ['tenant_id', 'timestamp'])
    op.create_index('ix_audit_entidad', 'audit_events', ['entidad', 'entidad_id'])
    op.create_index('ix_audit_correlation', 'audit_events', ['correlation_id'])


def downgrade() -> None:
    op.drop_table('audit_events')
    op.drop_table('snapshots_reporte')
    op.drop_table('alertas_gestion')
    op.drop_table('evidencias')
    op.drop_table('contrato_meta')
    op.drop_table('contratos_seguimiento')
    op.drop_table('ejecuciones_presupuestales')
    op.drop_table('presupuestos_proyecto')
    op.drop_table('proyecto_meta')
    op.drop_table('proyectos_inversion')
    op.drop_table('actividades_plan_accion')
    op.drop_table('planes_accion')
    op.drop_table('avances_metas')
    op.drop_table('programacion_anual_metas')
    op.drop_table('metas')
    op.drop_table('indicadores')
    op.drop_table('nodos_plan')
    op.drop_table('planes_desarrollo')
    op.drop_table('usuario_roles')
    op.drop_table('roles')
    op.drop_table('usuarios')
    op.drop_table('dependencias')
    op.drop_table('administraciones')
    op.drop_table('municipios')
    op.drop_table('tenants')
    op.execute("DROP EXTENSION IF EXISTS citext")
    op.execute("DROP EXTENSION IF EXISTS pgcrypto")
