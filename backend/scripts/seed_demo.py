"""Seed script completo para SIGM Colombia — datos demo."""
from __future__ import annotations

import asyncio
import uuid
from datetime import date

from app.core.database import async_session_factory
from app.core.security import hash_password
from app.models.administracion import Administracion
from app.models.control import AlertaGestion, Evidencia
from app.models.dependencia import Dependencia
from app.models.ejecucion import (
    ActividadPlanAccion,
    ContratoMeta,
    ContratoSeguimiento,
    EjecucionPresupuestal,
    PlanAccion,
    PresupuestoProyecto,
    ProyectoInversion,
    ProyectoMeta,
)
from app.models.municipio import Municipio
from app.models.plan_desarrollo import (
    AvanceMeta,
    Indicador,
    Meta,
    NodoPlan,
    PlanDesarrollo,
    ProgramacionAnualMeta,
)
from app.models.tenant import Tenant
from app.models.usuario import Rol, Usuario, UsuarioRol

TENANT_SLUG = "demo"
TENANT_ID = uuid.uuid4()
MUNICIPIO_ID = uuid.uuid4()
ADMIN_ID = uuid.uuid4()
DEPENDENCIA_PLANEACION_ID = uuid.uuid4()
DEPENDENCIA_OBRA_ID = uuid.uuid4()
USUARIO_ADMIN_ID = uuid.uuid4()
USUARIO_PLANEACION_ID = uuid.uuid4()
USUARIO_ALCALDE_ID = uuid.uuid4()
ROL_SUPERADMIN_ID = uuid.uuid4()
ROL_PLANEACION_ID = uuid.uuid4()
ROL_ALCALDE_ID = uuid.uuid4()


async def seed():
    async with async_session_factory() as db:
        try:
            # ── Tenant ──
            tenant = Tenant(
                id=TENANT_ID,
                nombre="Municipio Demo",
                slug=TENANT_SLUG,
                nit="890000000-0",
                estado="ACTIVO",
                configuracion={"timezone": "America/Bogota"},
            )
            db.add(tenant)

            # ── Municipio ──
            municipio = Municipio(
                id=MUNICIPIO_ID,
                tenant_id=TENANT_ID,
                codigo_dane="11001",
                nombre="Ciudad Demo",
                departamento="Cundinamarca",
                categoria="1",
                nit="890000000-0",
            )
            db.add(municipio)

            # ── Administración ──
            admin = Administracion(
                id=ADMIN_ID,
                tenant_id=TENANT_ID,
                municipio_id=MUNICIPIO_ID,
                nombre="Admin 2024-2027",
                alcalde_nombre="Juan Pérez",
                periodo_inicio=date(2024, 1, 1),
                periodo_fin=date(2027, 12, 31),
                estado="ACTIVA",
            )
            db.add(admin)

            # ── Dependencias ──
            dep_planeacion = Dependencia(
                id=DEPENDENCIA_PLANEACION_ID,
                tenant_id=TENANT_ID,
                codigo="DAPD",
                nombre="Departamento Administrativo de Planeación",
                tipo="SECRETARIA",
                estado="ACTIVA",
            )
            dep_obra = Dependencia(
                id=DEPENDENCIA_OBRA_ID,
                tenant_id=TENANT_ID,
                parent_id=DEPENDENCIA_PLANEACION_ID,
                codigo="DIOB",
                nombre="Dirección de Obras Públicas",
                tipo="DIRECCION",
                estado="ACTIVA",
            )
            db.add(dep_planeacion)
            db.add(dep_obra)

            # ── Roles ──
            rol_superadmin = Rol(
                id=ROL_SUPERADMIN_ID,
                tenant_id=TENANT_ID,
                nombre="SUPERADMIN",
                descripcion="Super administrador",
                es_sistema=True,
            )
            rol_planeacion = Rol(
                id=ROL_PLANEACION_ID,
                tenant_id=TENANT_ID,
                nombre="PLANEACION",
                descripcion="Funcionario de planeación",
                es_sistema=True,
            )
            rol_alcalde = Rol(
                id=ROL_ALCALDE_ID,
                tenant_id=TENANT_ID,
                nombre="ALCALDE",
                descripcion="Alcalde municipal",
                es_sistema=True,
            )
            db.add(rol_superadmin)
            db.add(rol_planeacion)
            db.add(rol_alcalde)

            # ── Usuarios ──
            usr_admin = Usuario(
                id=USUARIO_ADMIN_ID,
                tenant_id=TENANT_ID,
                dependencia_id=DEPENDENCIA_PLANEACION_ID,
                nombre_completo="Admin Demo",
                email="admin@demo.com",
                password_hash=hash_password("Admin123!"),
                estado="ACTIVO",
            )
            usr_planeacion = Usuario(
                id=USUARIO_PLANEACION_ID,
                tenant_id=TENANT_ID,
                dependencia_id=DEPENDENCIA_PLANEACION_ID,
                nombre_completo="Planeación Demo",
                email="planeacion@demo.com",
                password_hash=hash_password("Planeacion123!"),
                estado="ACTIVO",
            )
            usr_alcalde = Usuario(
                id=USUARIO_ALCALDE_ID,
                tenant_id=TENANT_ID,
                dependencia_id=DEPENDENCIA_PLANEACION_ID,
                nombre_completo="Alcalde Demo",
                email="alcalde@demo.com",
                password_hash=hash_password("Alcalde123!"),
                estado="ACTIVO",
            )
            db.add(usr_admin)
            db.add(usr_planeacion)
            db.add(usr_alcalde)

            # ── Usuario-Roles ──
            db.add(UsuarioRol(usuario_id=USUARIO_ADMIN_ID, rol_id=ROL_SUPERADMIN_ID))
            db.add(UsuarioRol(usuario_id=USUARIO_PLANEACION_ID, rol_id=ROL_PLANEACION_ID))
            db.add(UsuarioRol(usuario_id=USUARIO_ALCALDE_ID, rol_id=ROL_ALCALDE_ID))

            # ── Plan de Desarrollo ──
            plan_id = uuid.uuid4()
            plan = PlanDesarrollo(
                id=plan_id,
                tenant_id=TENANT_ID,
                administracion_id=ADMIN_ID,
                nombre="PDT 2024-2027",
                acuerdo_numero="Acuerdo 001",
                fecha_aprobacion=date(2024, 3, 15),
                vigencia_inicio=2024,
                vigencia_fin=2027,
                version=1,
                estado="APROBADO",
            )
            db.add(plan)

            # ── Nodos del Plan ──
            nodo_linea1_id = uuid.uuid4()
            nodo_linea2_id = uuid.uuid4()
            nodo_sector1_id = uuid.uuid4()

            nodo_linea1 = NodoPlan(
                id=nodo_linea1_id, tenant_id=TENANT_ID, plan_id=plan_id,
                tipo="LINEA_ESTRATEGICA", codigo="LE-01", nombre="Desarrollo Económico", orden=1,
            )
            nodo_linea2 = NodoPlan(
                id=nodo_linea2_id, tenant_id=TENANT_ID, plan_id=plan_id,
                tipo="LINEA_ESTRATEGICA", codigo="LE-02", nombre="Infraestructura", orden=2,
            )
            nodo_sector1 = NodoPlan(
                id=nodo_sector1_id, tenant_id=TENANT_ID, plan_id=plan_id,
                parent_id=nodo_linea1_id, tipo="SECTOR", codigo="SE-01", nombre="Turismo", orden=1,
            )
            db.add(nodo_linea1)
            db.add(nodo_linea2)
            db.add(nodo_sector1)

            # ── Indicadores ──
            ind1_id = uuid.uuid4()
            ind2_id = uuid.uuid4()
            ind1 = Indicador(
                id=ind1_id, tenant_id=TENANT_ID, codigo="IND-001",
                nombre="Turistas recibidos", tipo="PRODUCTO", unidad_medida="Personas",
                sentido="ASCENDENTE", periodicidad="ANUAL",
            )
            ind2 = Indicador(
                id=ind2_id, tenant_id=TENANT_ID, codigo="IND-002",
                nombre="Km vía mejorada", tipo="PRODUCTO", unidad_medida="Kilómetros",
                sentido="ASCENDENTE", periodicidad="ANUAL",
            )
            db.add(ind1)
            db.add(ind2)

            # ── Metas ──
            meta1_id = uuid.uuid4()
            meta2_id = uuid.uuid4()
            meta1 = Meta(
                id=meta1_id, tenant_id=TENANT_ID, nodo_plan_id=nodo_sector1_id,
                indicador_id=ind1_id, dependencia_id=DEPENDENCIA_PLANEACION_ID,
                codigo="META-001", descripcion="Incrementar turismo en 50%",
                meta_cuatrienio=50000, unidad_medida="Personas", estado="ACTIVA",
            )
            meta2 = Meta(
                id=meta2_id, tenant_id=TENANT_ID, nodo_plan_id=nodo_linea2_id,
                indicador_id=ind2_id, dependencia_id=DEPENDENCIA_OBRA_ID,
                codigo="META-002", descripcion="Mejorar 100 km de vías",
                meta_cuatrienio=100, unidad_medida="Kilómetros", estado="ACTIVA",
            )
            db.add(meta1)
            db.add(meta2)

            # ── Programación Anual ──
            for vig, val in [(2024, 10000), (2025, 12000), (2026, 14000), (2027, 14000)]:
                db.add(ProgramacionAnualMeta(
                    tenant_id=TENANT_ID, meta_id=meta1_id, vigencia=vig,
                    valor_programado=val, observacion=f"Programación {vig}",
                ))
            for vig, val in [(2024, 20), (2025, 30), (2026, 30), (2027, 20)]:
                db.add(ProgramacionAnualMeta(
                    tenant_id=TENANT_ID, meta_id=meta2_id, vigencia=vig,
                    valor_programado=val,
                ))

            # ── Avances ──
            for fc, vp, va in [
                ("2024-03-31", 2500, 2500), ("2024-06-30", 3000, 5500),
                ("2024-09-30", 2800, 8300), ("2024-12-31", 2200, 10500),
            ]:
                db.add(AvanceMeta(
                    tenant_id=TENANT_ID, meta_id=meta1_id, vigencia=2024,
                    periodo_tipo="TRIMESTRE", periodo_numero=1,
                    fecha_corte=date.fromisoformat(fc), valor_periodo=vp,
                    valor_acumulado=va, porcentaje_avance=int((va / 50000) * 100),
                    estado_revision="APROBADO",
                ))

            # ── Plan de Acción ──
            plan_accion_id = uuid.uuid4()
            db.add(PlanAccion(
                id=plan_accion_id, tenant_id=TENANT_ID,
                dependencia_id=DEPENDENCIA_PLANEACION_ID,
                vigencia=2026, nombre="PA Planeación 2026", version=1, estado="APROBADO",
            ))
            db.add(ActividadPlanAccion(
                tenant_id=TENANT_ID, plan_accion_id=plan_accion_id,
                meta_id=meta1_id, responsable_usuario_id=USUARIO_PLANEACION_ID,
                descripcion="Ejecutar campaña de turismo",
                fecha_inicio=date(2026, 1, 1), fecha_fin=date(2026, 6, 30),
                presupuesto_estimado=50000000, porcentaje_avance=30, estado="EN_EJECUCION",
            ))

            # ── Proyecto de Inversión ──
            proyecto_id = uuid.uuid4()
            db.add(ProyectoInversion(
                id=proyecto_id, tenant_id=TENANT_ID, codigo_interno="PRY-001",
                codigo_bpin="BPIN-20240001234",
                nombre="Mejoramiento Vía Principal",
                objetivo="Mejorar la infraestructura vial del municipio",
                dependencia_id=DEPENDENCIA_OBRA_ID,
                vigencia_inicio=2024, vigencia_fin=2027,
                estado="EJECUCION", fuente_origen="PIIP",
            ))
            db.add(ProyectoMeta(
                proyecto_id=proyecto_id, meta_id=meta2_id,
                peso_aporte=70, observacion="Proyecto principal de vías",
            ))

            # ── Presupuesto ──
            pres_id = uuid.uuid4()
            db.add(PresupuestoProyecto(
                id=pres_id, tenant_id=TENANT_ID, proyecto_id=proyecto_id,
                vigencia=2026, fuente="Recursos Propios",
                apropiacion_inicial=500000000, adiciones=0, reducciones=0,
                apropiacion_definitiva=500000000, origen_dato="MANUAL",
            ))

            # ── Ejecución Presupuestal ──
            db.add(EjecucionPresupuestal(
                tenant_id=TENANT_ID, presupuesto_id=pres_id,
                fecha_corte=date(2026, 6, 30), cdp=200000000,
                rp_compromisos=180000000, obligaciones=150000000,
                pagos=120000000, porcentaje_ejecucion=24, origen_dato="MANUAL",
            ))

            # ── Contrato ──
            contrato_id = uuid.uuid4()
            db.add(ContratoSeguimiento(
                id=contrato_id, tenant_id=TENANT_ID, proyecto_id=proyecto_id,
                numero="CONT-2026-001", objeto="Construcción de vía",
                contratista="Constructora ABC S.A.S",
                supervisor_usuario_id=USUARIO_ADMIN_ID,
                fecha_inicio=date(2026, 3, 1), fecha_fin=date(2026, 12, 31),
                valor_inicial=300000000, valor_actual=300000000,
                avance_fisico=35, avance_financiero=28, estado="EJECUCION",
            ))
            db.add(ContratoMeta(
                contrato_id=contrato_id, meta_id=meta2_id,
                aporte_estimado=60, observacion="Contrato de vías",
            ))

            # ── Evidencias ──
            db.add(Evidencia(
                tenant_id=TENANT_ID, entidad_tipo="META", entidad_id=meta1_id,
                nombre_archivo="fotografia_turismo.jpg",
                storage_uri="evidencias/2024/turismo.jpg",
                mime_type="image/jpeg", tamano_bytes=2048000,
                sha256="abc123hash", clasificacion="PUBLICA", version=1,
            ))

            # ── Alertas ──
            db.add(AlertaGestion(
                tenant_id=TENANT_ID, tipo="META_ATRASADA", severidad="MEDIA",
                entidad_tipo="META", entidad_id=str(meta2_id),
                mensaje="Meta de vías con bajo avance físico",
                estado="ABIERTA", regla_version="1.0",
            ))

            await db.commit()
            print("✓ Seed completado exitosamente")
            print(f"  Tenant: {TENANT_SLUG}")
            print("  Usuarios: admin@demo.com, planeacion@demo.com, alcalde@demo.com")
            print("  Plan de Desarrollo: PDT 2024-2027")
            print("  Metas: 2 | Proyectos: 1 | Contratos: 1")

        except Exception as e:
            await db.rollback()
            print(f"✗ Error en seed: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(seed())
