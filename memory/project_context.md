# Contexto del Proyecto

## Objetivo
SIGM Colombia: Sistema Integral de Gestión Municipal. Plataforma SaaS multi-tenant para Alcaldías colombianas.

## Estado actual
Backend completo (Fases 1-13). Frontend completado con CRUD funcional.

## Arquitectura
FastAPI + SQLAlchemy 2 + PostgreSQL + Next.js. Multi-tenant desde el origen.

## Backend
- Python 3.12+, FastAPI, SQLAlchemy 2, Alembic, Pydantic 2
- Auth: JWT + Argon2id
- Repositories con filtro tenant_id
- 60+ API endpoints funcionales

## Frontend
- Next.js 15 + React 19 + TypeScript + Tailwind CSS
- Auth: Login con JWT, persistencia localStorage
- Dashboard: Resumen gerencial (6 KPIs)
- Planeación CRUD: Planes, nodos jerárquicos, indicadores, metas, avances, programación
- Ejecución CRUD: Proyectos, contratos, presupuestos
- Control: Alertas con filtro y workflow
- Reportes: Avance por meta con progreso
- Dockerfile multi-stage para producción
- Build exitoso: 122 kB first load

## Base de datos
PostgreSQL 17+. 25 tablas definidas y migradas.

## Módulos implementados

### Planeación (Fases 1-4)
- Planes de Desarrollo, Nodos jerárquicos (adjacency list)
- Indicadores, Metas, Programación Anual, Avances

### Ejecución (Fases 5-6)
- Planes de Acción por dependencia/vigencia
- Actividades operativas con seguimiento de avance
- Proyectos de Inversión con código BPIN
- Relación Proyecto-Meta (N:M)

### Presupuesto y Financiero (Fase 8)
- Presupuestos por proyecto/vigencia/fuente
- Ejecución presupuestal (CDP, RP, obligaciones, pagos)
- Cálculo automático de porcentaje de ejecución

### Contratos (Fase 6)
- Seguimiento interno contractual
- Relación Contrato-Meta (N:M)
- Estados: PLANEADO/EJECUCION/SUSPENDIDO/TERMINADO/LIQUIDADO

### Alertas y Control (Fase 9)
- Alertas de gestión (META_ATRASADA, DESVIACION_FISICO_FINANCIERA)
- Evaluación automática de desviaciones
- Workflow: ABIERTA → ATENDIDA → CERRADA

### Evidencias y Snapshots (Fase 10)
- Evidencias polimórficas (META/AVANCE/ACTIVIDAD/PROYECTO/CONTRATO)
- Versionamiento documental
- Snapshots de corte con hash de integridad
- Aprobación de snapshots

### Dashboard (Fase 11)
- Resumen gerencial: planes, metas, proyectos, contratos, alertas

### Reportes (Fase 12)
- Reporte de avance por meta con programación y avances

### Auditoría (Fase 13)
- Eventos de auditoría inmutables
- Trazabilidad por entidad y correlación

## Usuarios demo
- admin@demo.com / Admin123! (SUPERADMIN)
- planeacion@demo.com / Planeacion123! (PLANEACION)
- alcalde@demo.com / Alcalde123! (ALCALDE)

## Riesgos conocidos
- Tests de integración requieren PostgreSQL activo
- CI/CD pendiente de configurar
