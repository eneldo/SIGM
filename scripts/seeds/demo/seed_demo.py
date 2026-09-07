#!/usr/bin/env python3
"""Seed script para crear tenant demo y usuario admin."""
from __future__ import annotations

import asyncio
import uuid
from datetime import date

from app.core.database import async_session_factory
from app.core.security import hash_password
from app.models import (
    Administracion,
    Dependencia,
    Municipio,
    PlanDesarrollo,
    Rol,
    Tenant,
    Usuario,
    UsuarioRol,
)


async def seed_demo():
    async with async_session_factory() as db:
        try:
            # Tenant demo
            tenant = Tenant(
                id=uuid.uuid4(),
                nombre="Alcaldía Demo",
                slug="demo",
                nit="900123456-7",
                estado="ACTIVO",
                configuracion={"moneda": "COP", "timezone": "America/Bogota"},
            )
            db.add(tenant)
            await db.flush()

            # Municipio
            municipio = Municipio(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                codigo_dane="11001",
                nombre="Bogotá D.C.",
                departamento="Cundinamarca",
                categoria="Especial",
            )
            db.add(municipio)
            await db.flush()

            # Administración
            admin = Administracion(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                municipio_id=municipio.id,
                nombre="Municipio Avanza 2024-2027",
                alcalde_nombre="Juan Pérez",
                periodo_inicio=date(2024, 1, 1),
                periodo_fin=date(2027, 12, 31),
                estado="ACTIVA",
            )
            db.add(admin)
            await db.flush()

            # Dependencias
            despacho = Dependencia(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                codigo="DESP-001",
                nombre="Despacho del Alcalde",
                tipo="DESPACHO",
                estado="ACTIVA",
            )
            db.add(despacho)

            planeacion = Dependencia(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                parent_id=despacho.id,
                codigo="SEC-PLN",
                nombre="Secretaría de Planeación",
                tipo="SECRETARIA",
                estado="ACTIVA",
            )
            db.add(planeacion)

            hacienda = Dependencia(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                parent_id=despacho.id,
                codigo="SEC-HAC",
                nombre="Secretaría de Hacienda",
                tipo="SECRETARIA",
                estado="ACTIVA",
            )
            db.add(hacienda)
            await db.flush()

            # Roles
            roles_data = [
                ("SUPERADMIN", "Superadministrador del sistema"),
                ("ADMIN_ENTIDAD", "Administrador de la entidad"),
                ("ALCALDE", "Alcalde municipal"),
                ("PLANEACION", "Secretaría de Planeación"),
                ("HACIENDA", "Secretaría de Hacienda"),
                ("RESPONSABLE_PROYECTO", "Responsable de proyecto"),
                ("CONSULTA", "Solo consulta"),
            ]
            roles = {}
            for nombre, desc in roles_data:
                rol = Rol(
                    id=uuid.uuid4(),
                    tenant_id=tenant.id,
                    nombre=nombre,
                    descripcion=desc,
                    es_sistema=True,
                )
                db.add(rol)
                roles[nombre] = rol
            await db.flush()

            # Usuarios demo
            admin_user = Usuario(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                dependencia_id=despacho.id,
                nombre_completo="Administrador Demo",
                email="admin@demo.com",
                password_hash=hash_password("Admin123!"),
                estado="ACTIVO",
            )
            db.add(admin_user)

            planeacion_user = Usuario(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                dependencia_id=planeacion.id,
                nombre_completo="Planeación Demo",
                email="planeacion@demo.com",
                password_hash=hash_password("Planeacion123!"),
                estado="ACTIVO",
            )
            db.add(planeacion_user)

            alcalde_user = Usuario(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                dependencia_id=despacho.id,
                nombre_completo="Alcalde Demo",
                email="alcalde@demo.com",
                password_hash=hash_password("Alcalde123!"),
                estado="ACTIVO",
            )
            db.add(alcalde_user)
            await db.flush()

            # Asignar roles
            db.add(UsuarioRol(usuario_id=admin_user.id, rol_id=roles["SUPERADMIN"].id))
            db.add(UsuarioRol(usuario_id=admin_user.id, rol_id=roles["ADMIN_ENTIDAD"].id))
            db.add(UsuarioRol(usuario_id=planeacion_user.id, rol_id=roles["PLANEACION"].id))
            db.add(UsuarioRol(usuario_id=alcalde_user.id, rol_id=roles["ALCALDE"].id))
            await db.flush()

            # Plan de Desarrollo
            plan = PlanDesarrollo(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                administracion_id=admin.id,
                nombre="Municipio Avanza 2024-2027",
                acuerdo_numero="Acuerdo 001 de 2024",
                vigencia_inicio=2024,
                vigencia_fin=2027,
                version=1,
                estado="APROBADO",
            )
            db.add(plan)
            await db.flush()

            await db.commit()
            print("[OK] Seed demo creado exitosamente")
            print(f"     Tenant: {tenant.slug}")
            print(f"     Admin: admin@demo.com / Admin123!")
            print(f"     Planeación: planeacion@demo.com / Planeacion123!")
            print(f"     Alcalde: alcalde@demo.com / Alcalde123!")
        except Exception as e:
            await db.rollback()
            print(f"[ERROR] {e}")
            raise


if __name__ == "__main__":
    asyncio.run(seed_demo())
