# ADR-0001: Stack tecnológico SIGM Colombia V1

## Estado
Aceptado

## Contexto
SIGM Colombia requiere un stack tecnológico que soporte:
- Multi-tenant desde el origen
- Alta integridad de datos (PostgreSQL)
- API-first (FastAPI)
- Frontend moderno y accesible (Next.js)
- Escalabilidad y mantenibilidad

## Decisión
Usar:
- Python 3.12+ / FastAPI / SQLAlchemy 2 / Alembic / Pydantic 2
- PostgreSQL 17+
- Next.js / React / TypeScript
- Docker / Docker Compose

## Consecuencias
- Positivo: Stack probado, gran ecosistema, tipado fuerte
- Negativo: Curva de aprendizaje en SQLAlchemy 2 async
- Riesgo: Mantener sincronización entre modelos y documentación ER

## Documentos de soporte
- docs/01_ALCANCE_ARQUITECTURA_V1.md §6
- docs/02_ER_DICCIONARIO_DATOS_V1.md §2
