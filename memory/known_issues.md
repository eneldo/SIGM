# Problemas Conocidos

### ISSUE-0001 — Pendiente migración Alembic

**Estado:** PENDING

**Síntoma:**
La migración inicial fue creada pero no ejecutada. Requiere PostgreSQL corriendo.

**Causa:**
Proyecto en fase de desarrollo, sin acceso a base de datos en este momento.

**Solución o mitigación:**
Ejecutar `alembic upgrade head` cuando PostgreSQL esté disponible.

**Prevención:**
Verificar entorno de base de datos antes de cada fase.

### ISSUE-0002 — Frontend pendiente

**Estado:** PENDING

**Síntoma:**
No existe código de frontend. Solo estructura de directorios.

**Causa:**
Enfoque en backend primero según documento de alcance.

**Solución o mitigación:**
Implementar frontend después de completar Fase 10 (módulos core).

**Prevención:**
Seguir orden de fases del documento de alcance.

### ISSUE-0003 — Tests incompletos

**Estado:** PENDING

**Síntoma:**
Solo existen tests básicos de autenticación y aislamiento.

**Causa:**
Prioridad en funcionalidad sobre cobertura de tests.

**Solución o mitigación:**
Completar tests unitarios y de integración por módulo.

**Prevención:**
Crear tests junto con cada nueva funcionalidad.
