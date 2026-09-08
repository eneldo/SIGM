from datetime import date
import uuid
import asyncio
import sys
sys.path.insert(0, r'F:\SIGM\backend')

from app.core.database import async_session_factory, engine
from app.models.legal import NormaLegal, RequisitoLegal
from app.schemas.legal import NormaLegalCreate, RequisitoLegalCreate
from app.services.legal import LegalService
from app.models.usuario import Usuario
from app.models.dependencia import Dependencia
from sqlalchemy import select


async def seed_legal_matrix():
    async with async_session_factory() as db:
        service = LegalService(db)

        # Buscar usuario admin y dependencia
        usuario_result = await db.execute(select(Usuario).where(Usuario.estado == "ACTIVO"))
        usuario = usuario_result.scalar_one_or_none()

        dependencia_result = await db.execute(select(Dependencia).limit(1))
        dependencia = dependencia_result.scalar_one_or_none()

        print(f"Usuario admin: {usuario}")
        print(f"Dependencia: {dependencia}")

        # 15 normas legales base
        normas_base = [
            {
                "tipo": "LEY",
                "numero": "Ley 142",
                "titulo": "Ley de Presupuesto General",
                "entidad_emisora": "Congreso de la República",
                "fecha_expedicion": date(2020, 1, 1),
                "fuente": "Congreso",
                "vigencia_desde": date(2020, 1, 1),
                "vigencia_hasta": date(2025, 12, 31),
                "fuente_url": "https://www.congreso.gov.co/ley142",
            },
            {
                "tipo": "DECRETO",
                "numero": "Decreto 1234",
                "titulo": "Reglamento de la Ley de Presupuesto",
                "entidad_emisora": "Presidencia",
                "fecha_expedicion": date(2020, 3, 15),
                "fuente": "Presidencia",
                "vigencia_desde": date(2020, 3, 15),
                "fuente_url": "https://www.presidencia.gov.decreto1234",
            },
            {
                "tipo": "ACUERDO",
                "numero": "AC-001",
                "titulo": "Acuerdo de Planificación",
                "entidad_emisora": "Alcaldía",
                "fecha_expedicion": date(2021, 6, 1),
                "fuente": "Alcaldía",
                "vigencia_desde": date(2021, 6, 1),
                "fuente_url": None,
            },
            {
                "tipo": "LEY",
                "numero": "Ley 194",
                "titulo": "Ley de Planeación",
                "entidad_emisora": "Congreso de la República",
                "fecha_expedicion": date(2019, 6, 1),
                "fuente": "Congreso",
                "vigencia_desde": date(2019, 6, 1),
                "vigencia_hasta": None,
                "fuente_url": "https://www.congreso.gov.co/ley194",
            },
            {
                "tipo": "DECRETO",
                "numero": "Decreto 5678",
                "titulo": "Presupuesto Participativo",
                "entidad_emisora": "Alcaldía",
                "fecha_expedicion": date(2022, 1, 1),
                "fuente": "Alcaldía",
                "vigencia_desde": date(2022, 1, 1),
                "vigencia_hasta": date(2026, 12, 31),
                "fuente_url": None,
            },
            {
                "tipo": "RESOLUCION",
                "numero": "Res-2023-001",
                "titulo": "Reglamento de Transparencia",
                "entidad_emisora": "Contraloría",
                "fecha_expedicion": date(2023, 2, 10),
                "fuente": "Contraloría",
                "vigencia_desde": date(2023, 2, 10),
                "vigencia_hasta": None,
                "fuente_url": None,
            },
            {
                "tipo": "LEY",
                "numero": "Ley 54",
                "titulo": "Código de Comercio",
                "entidad_emisora": "Congreso de la República",
                "fecha_expedicion": date(1999, 1, 1),
                "fuente": "Congreso",
                "vigencia_desde": date(1999, 1, 1),
                "vigencia_hasta": None,
                "fuente_url": "https://www.congreso.gov.co/ley54",
            },
            {
                "tipo": "DECRETO",
                "numero": "Decreto 901",
                "titulo": "Organización Administrativa",
                "entidad_emisora": "Presidencia",
                "fecha_expedicion": date(2018, 11, 1),
                "fuente": "Presidencia",
                "vigencia_desde": date(2018, 11, 1),
                "vigencia_hasta": None,
                "fuente_url": None,
            },
            {
                "tipo": "ACUERDO",
                "numero": "AC-010",
                "titulo": "Plan de Desarrollo 2024-2027",
                "entidad_emisora": "Alcaldía",
                "fecha_expedicion": date(2023, 1, 15),
                "fuente": "Alcaldía",
                "vigencia_desde": date(2023, 1, 15),
                "vigencia_hasta": date(2027, 12, 31),
                "fuente_url": None,
            },
            {
                "tipo": "LEY",
                "numero": "Ley 21",
                "titulo": "Lei Orgánica de Finanzas Públicas",
                "entidad_emisora": "Congreso de la República",
                "fecha_expedicion": date(2005, 7, 1),
                "fuente": "Congreso",
                "vigencia_desde": date(2005, 7, 1),
                "vigencia_hasta": None,
                "fuente_url": "https://www.congreso.gov.co/ley21",
            },
            {
                "tipo": "DECRETO",
                "numero": "Decreto 345",
                "titulo": "Régimen de Contratación",
                "entidad_emisora": "Alcaldía",
                "fecha_expedicion": date(2021, 5, 20),
                "fuente": "Alcaldía",
                "vigencia_desde": date(2021, 5, 20),
                "vigencia_hasta": date(2025, 12, 31),
                "fuente_url": None,
            },
            {
                "tipo": "RESOLUCION",
                "numero": "Res-2024-015",
                "titulo": "Manual de Funciones",
                "entidad_emisora": "Secretaría de Hacienda",
                "fecha_expedicion": date(2024, 3, 1),
                "fuente": "Secretaría de Hacienda",
                "vigencia_desde": date(2024, 3, 1),
                "vigencia_hasta": None,
                "fuente_url": None,
            },
            {
                "tipo": "ACUERDO",
                "numero": "AC-020",
                "titulo": "Política de Contrataciones Públicas",
                "entidad_emisora": "Alcaldía",
                "fecha_expedicion": date(2022, 8, 1),
                "fuente": "Alcaldía",
                "vigencia_desde": date(2022, 8, 1),
                "vigencia_hasta": date(2026, 12, 31),
                "fuente_url": None,
            },
            {
                "tipo": "LEY",
                "numero": "Ley 13",
                "titulo": "Ley de Transparencia y Acceso a la Información",
                "entidad_emisora": "Congreso de la República",
                "fecha_expedicion": date(2011, 5, 1),
                "fuente": "Congreso",
                "vigencia_desde": date(2011, 5, 1),
                "vigencia_hasta": None,
                "fuente_url": "https://www.congreso.gov.co/ley13",
            },
            {
                "tipo": "DECRETO",
                "numero": "Decreto 789",
                "titulo": "Reglamento de la Ley de Transparencia",
                "entidad_emisora": "Contraloría",
                "fecha_expedicion": date(2012, 3, 15),
                "fuente": "Contraloría",
                "vigencia_desde": date(2012, 3, 15),
                "vigencia_hasta": date(2025, 12, 31),
                "fuente_url": None,
            },
        ]

        # Insertar normas
        normas_creadas = []
        for i, norma_data in enumerate(normas_base):
            norma_create = NormaLegalCreate(**norma_data)
            norma = await service.create_norma(
                str(usuario.id) if usuario else "00000000-0000-0000-0000-000000000000",
                norma_create.model_dump()
            )
            normas_creadas.append(norma)
            print(f"Norma {i+1} creada: {norma.numero} - {norma.titulo[:50]}")

        # Requisitos asociados a cada norma (2-3 por norma)
        estados_cumplimiento = ["PENDIENTE", "CUMPLE", "NO_CUMPLE", "NO_APLICA"]
        for idx, norma in enumerate(normas_creadas):
            # 2 o 3 requisitos por norma
            num_req = 2 + idx % 3
            for j in range(num_req):
                req_codigo = f"REQ-{norma.id[:8]}-{j+1:02d}"
                req_desc = f"Requisito asociado a {norma.titulo[:30]}..."
                dep_id = str(dependencia.id) if dependencia else "00000000-0000-0000-0000-000000000000"
                user_id = str(usuario.id) if usuario else "00000000-0000-0000-0000-000000000000"

                req_create = RequisitoLegalCreate(
                    norma_legal_id=norma.id,
                    codigo=req_codigo,
                    descripcion=req_desc,
                    aplica=True,
                    responsable_dependencia_id=uuid.UUID(dep_id),
                    responsable_usuario_id=uuid.UUID(user_id),
                    estado_cumplimiento=estados_cumplimiento[j % 4],
                    fecha_evaluacion=date.today() if j % 2 == 0 else None,
                    proxima_revision=date.today().replace(year=date.today().year + 1) if j % 3 != 0 else None,
                    observaciones=f"Observación del requisito {j+1} para {norma.titulo[:20]}",
                )
                req = await service.create_requisito(
                    str(usuario.id) if usuario else "00000000-0000-0000-0000-000000000000",
                    req_create.model_dump()
                )
                print(f"  Requisito {j+1} creado: {req.codigo} - {req.estado_cumplimiento}")

        await db.commit()
        print("\nSeed de matriz legal completado exitosamente!")


if __name__ == "__main__":
    asyncio.run(seed_legal_matrix())