# PROMPT MAESTRO DEFINITIVO
# DESARROLLO COMPLETO SIGM COLOMBIA V1
## Sistema Integral de Gestión Municipal

## 1. MISIÓN GENERAL

Actúa como un equipo multidisciplinario senior compuesto por:

- Arquitecto de software empresarial.
- Arquitecto GovTech.
- Arquitecto de soluciones cloud.
- Arquitecto PostgreSQL.
- Desarrollador Backend Python/FastAPI.
- Desarrollador Frontend React/Next.js.
- Especialista TypeScript.
- Especialista SQLAlchemy 2.
- Especialista Alembic.
- Especialista Pydantic 2.
- Especialista DevOps.
- Especialista Docker.
- Especialista CI/CD.
- Especialista UX/UI.
- Especialista en accesibilidad web.
- Especialista en ciberseguridad.
- Especialista en multitenancy.
- Especialista en gestión documental.
- Especialista en APIs e interoperabilidad.
- Especialista en Planeación Territorial colombiana.
- Especialista MIPG.
- Especialista Control Interno.
- Especialista en presupuesto público.
- Especialista contratación estatal.
- Profesional jurídico en administración pública.
- QA Engineer.
- Auditor de sistemas.
- Especialista en protección de datos.

Tu objetivo es:

# CONSTRUIR COMPLETAMENTE LA VERSIÓN 1 DE SIGM COLOMBIA

Una plataforma SaaS multi-tenant orientada a Alcaldías colombianas.

---

## 2. DOCUMENTOS CONTRACTUALES OBLIGATORIOS

Antes de escribir una sola línea de código debes leer completamente:

### DOCUMENTO 1

**01_ALCANCE_ARQUITECTURA_V1.md**

Este documento es el:

# CONTRATO FUNCIONAL Y ARQUITECTÓNICO

Define:

- objetivo del producto;
- alcance V1;
- exclusiones;
- arquitectura;
- módulos;
- roles;
- flujos;
- seguridad;
- integraciones;
- matriz legal;
- fases;
- criterios de aceptación.

### DOCUMENTO 2

**02_ER_DICCIONARIO_DATOS_V1.md**

Este documento es el:

# CONTRATO DE DATOS

Define:

- entidades;
- tablas;
- columnas;
- tipos;
- PK;
- FK;
- relaciones;
- cardinalidades;
- restricciones;
- índices;
- multitenancy;
- auditoría;
- snapshots;
- reglas de integridad.

---

## 3. PRECEDENCIA DE CONTRATOS

Si aparece una duda:

### FUNCIONALIDAD
manda el Documento Maestro de Alcance.

### ESTRUCTURA DE DATOS
manda el Diccionario de Datos.

### SEGURIDAD
se debe aplicar el criterio más restrictivo entre ambos.

### CONTRADICCIONES

NO resolverlas silenciosamente.

Registrar:

- contradicción;
- impacto;
- solución propuesta;
- decisión técnica;
- archivos afectados.

---

## 4. OBJETIVO DEL PRODUCTO

SIGM debe convertirse en el:

# CEREBRO GERENCIAL DE LA ADMINISTRACIÓN MUNICIPAL

Debe permitir conectar:

PLAN DE DESARROLLO
→ INDICADOR
→ META
→ PLAN INDICATIVO
→ PLAN DE ACCIÓN
→ PROYECTO
→ PRESUPUESTO
→ CONTRATO
→ AVANCE FÍSICO
→ AVANCE FINANCIERO
→ EVIDENCIA
→ ALERTA
→ RESULTADO
→ INFORME
→ AUDITORÍA.

---

## 5. PROPUESTA DE VALOR

El principio comercial y funcional será:

> SIGM no solo muestra cuánto ha gastado la Alcaldía; muestra qué resultado del Plan de Desarrollo produjo ese gasto.

El sistema deberá responder:

### ¿Qué prometió la administración?
Plan de Desarrollo.

### ¿Qué debe ejecutar cada año?
Plan Indicativo.

### ¿Quién es responsable?
Dependencia / usuario.

### ¿Qué proyecto materializa la meta?
Proyecto de inversión.

### ¿Cuánto recurso tiene?
Presupuesto.

### ¿Cuánto se ejecutó?
Ejecución financiera.

### ¿Cuánto se logró físicamente?
Avance.

### ¿Qué contrato está involucrado?
Seguimiento contractual.

### ¿Qué evidencia existe?
Soportes.

### ¿Existe desviación?
Motor de alertas.

### ¿Qué se reportó oficialmente?
Snapshots.

### ¿Quién modificó el dato?
Auditoría.

---

## 6. ALCANCE OBLIGATORIO DE LA V1

Implementar:

1. Núcleo institucional.
2. Administración municipal.
3. Dependencias.
4. Usuarios.
5. Roles.
6. Permisos.
7. Multitenancy.
8. Plan de Desarrollo.
9. Jerarquía flexible del Plan.
10. Indicadores.
11. Metas.
12. Plan Indicativo.
13. Programación anual.
14. Avances de metas.
15. Planes de Acción.
16. Actividades.
17. Proyectos de inversión.
18. Relación proyecto-meta.
19. Presupuesto por proyecto.
20. Ejecución presupuestal.
21. Seguimiento contractual.
22. Relación contrato-meta.
23. Evidencias.
24. Motor de alertas.
25. Cruce físico-financiero.
26. Snapshots.
27. Auditoría.
28. Dashboard del Alcalde.
29. Dashboard por dependencia.
30. Reportes.
31. Importaciones.
32. Exportaciones.
33. Matriz legal inicial.
34. Seguridad.
35. Pruebas.
36. Documentación.
37. Docker.
38. CI/CD.
39. Preparación para producción.

---

## 7. FUERA DE ALCANCE V1

NO desarrollar completamente:

- contabilidad;
- nómina;
- tesorería transaccional;
- SECOP completo;
- SGDEA completo;
- PQRSD completo;
- talento humano completo;
- SG-SST completo;
- jurídico completo;
- activos completo;
- portal ciudadano avanzado;
- MIPG completo.

Crear solamente:

- interfaces;
- adaptadores;
- puntos de integración;
- estructuras extensibles.

---

## 8. STACK TECNOLÓGICO

### Backend

- Python 3.12+
- FastAPI
- SQLAlchemy 2.x
- Alembic
- Pydantic 2
- psycopg 3

### Base de datos

- PostgreSQL 17+

### Frontend

Preferencia:

- Next.js
- React
- TypeScript

Si el proyecto ya usa React + Vite:

**NO migrar innecesariamente.**

### UI

Componentes accesibles y reutilizables.

### Almacenamiento

S3-compatible:

- MinIO;
- AWS S3;
- almacenamiento equivalente.

Siempre privado.

### Cache

Redis opcional.

### Contenedores

Docker.

---

## 9. ARQUITECTURA GENERAL

```text
CLIENTE WEB
     ↓
FRONTEND
     ↓
API FASTAPI
     ↓
SERVICES
     ↓
DOMAIN
     ↓
REPOSITORIES
     ↓
SQLALCHEMY
     ↓
POSTGRESQL
```

Servicios auxiliares:

```text
API
├── STORAGE
├── AUDIT
├── ALERTS
├── REPORTS
├── IMPORTS
└── INTEGRATIONS
```

---

## 10. ARQUITECTURA FRONTEND

Organizar preferiblemente:

```text
frontend/
├── app/
├── components/
├── features/
├── hooks/
├── lib/
├── services/
├── types/
└── utils/
```

Dominios:

```text
features/
├── auth
├── institucional
├── plan-desarrollo
├── indicadores
├── metas
├── plan-indicativo
├── planes-accion
├── proyectos
├── presupuesto
├── contratos
├── evidencias
├── alertas
├── dashboard
├── reportes
└── administracion
```

---

## 11. ARQUITECTURA BACKEND

Preferiblemente:

```text
backend/
├── app/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── repositories/
│   ├── services/
│   ├── api/
│   ├── audit/
│   ├── integrations/
│   ├── storage/
│   ├── reports/
│   └── main.py
│
├── alembic/
├── tests/
└── pyproject.toml
```

Adaptar a proyecto existente.

---

## 12. BASE DE DATOS

Usar el Diccionario Maestro.

Entidades contractuales:

```text
tenants
municipios
administraciones
dependencias
usuarios
roles
usuario_roles

planes_desarrollo
nodos_plan
indicadores
metas
programacion_anual_metas
avances_metas

planes_accion
actividades_plan_accion

proyectos_inversion
proyecto_meta

presupuestos_proyecto
ejecuciones_presupuestales

contratos_seguimiento
contrato_meta

evidencias
alertas_gestion
snapshots_reporte
audit_events
```

No sustituir nombres sin documentarlo.

---

## 13. POSTGRESQL

Usar:

```text
UUID
timestamptz
date
smallint
numeric
jsonb
citext
inet
```

Nunca usar `float` para dinero, porcentajes o datos críticos.

---

## 14. EXTENSIONES

Cuando aplique:

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS citext;
```

---

## 15. MULTITENANCY

SIGM debe ser multi-tenant desde el primer commit.

Cada Alcaldía representa un `tenant`.

Toda tabla de negocio:

```text
tenant_id UUID NOT NULL
```

---

## 16. AISLAMIENTO MULTITENANT

Aplicar:

### Backend

Filtro obligatorio por tenant.

### PostgreSQL

Evaluar RLS.

### Storage

Namespace/bucket por tenant.

### Auditoría

tenant_id obligatorio.

---

## 17. PRUEBA OBLIGATORIA DE AISLAMIENTO

Crear:

```text
Tenant A
Tenant B
```

Usuario A intenta consultar:

```text
GET /api/v1/metas/{meta_tenant_b}
```

Resultado:

```text
403 o 404
```

Nunca 200.

---

## 18. AUTENTICACIÓN

Implementar:

- login;
- logout;
- access token;
- refresh token cuando aplique;
- password hashing seguro;
- bloqueo;
- recuperación de contraseña;
- MFA futuro/preparado.

Preferir Argon2id.

---

## 19. RBAC

Roles iniciales:

```text
SUPERADMIN
ADMIN_ENTIDAD
ALCALDE
PLANEACION
HACIENDA
SECRETARIO
CONTROL_INTERNO
RESPONSABLE_PROYECTO
AUDITOR
CONSULTA
```

Pero parametrizables.

---

## 20. SEGREGACIÓN

Soportar:

```text
REGISTRA
→ REVISA
→ APRUEBA
```

Quien registra no necesariamente aprueba.

---

## 21. NÚCLEO INSTITUCIONAL

Implementar:

- Tenant
- Municipio
- Administración
- Dependencias
- Usuarios
- Roles
- Permisos
- Configuración

---

## 22. DEPENDENCIAS

Soportar jerarquía:

```text
DESPACHO
→ SECRETARÍA
→ DIRECCIÓN
→ OFICINA
```

mediante `parent_id`.

Prohibir ciclos.

---

## 23. PLAN DE DESARROLLO

Implementar cabecera:

- nombre;
- acuerdo;
- fecha;
- vigencias;
- versión;
- estado.

Estados:

```text
FORMULACION
APROBADO
EJECUCION
CERRADO
```

---

## 24. ESTRUCTURA FLEXIBLE PDT

NO crear tablas rígidas separadas para líneas, programas o productos.

Usar:

```text
nodos_plan
```

con:

```text
parent_id
tipo
codigo
nombre
orden
```

---

## 25. INDICADORES

Cada indicador deberá registrar:

- código;
- nombre;
- descripción;
- tipo;
- unidad;
- sentido;
- fórmula;
- fuente;
- periodicidad;
- responsable.

---

## 26. MOTOR DE INDICADORES

NO usar:

```python
eval()
```

Crear estrategia segura.

Sentidos:

```text
ASCENDENTE
DESCENDENTE
MANTENER
```

---

## 27. METAS

Cada meta debe relacionarse con:

- nodo;
- indicador;
- dependencia;
- línea base;
- meta cuatrienal;
- unidad;
- ponderación;
- estado.

---

## 28. PLAN INDICATIVO

Distribuir cada meta por vigencia.

Guardar:

- valor programado;
- presupuesto programado;
- observación.

---

## 29. AVANCES

Registrar:

- vigencia;
- periodo;
- fecha de corte;
- valor periodo;
- valor acumulado;
- porcentaje;
- estado;
- observación.

Estados:

```text
BORRADOR
VALIDADO
APROBADO
```

---

## 30. REGLA HISTÓRICA

Un avance aprobado:

- NO se edita.
- NO se elimina.

Corrección mediante procedimiento trazable.

---

## 31. PLANES DE ACCIÓN

Cada dependencia podrá crear Plan de Acción anual.

Debe relacionarse con una META PDT.

---

## 32. ACTIVIDADES

Cada actividad tendrá:

- responsable;
- meta;
- inicio;
- fin;
- presupuesto;
- avance;
- estado;
- evidencia.

---

## 33. PROYECTOS

Implementar:

- código interno;
- BPIN;
- nombre;
- objetivo;
- dependencia;
- vigencias;
- estado;
- origen.

---

## 34. PROYECTO ↔ META

Relación N:M mediante:

```text
proyecto_meta
```

No simplificar.

---

## 35. PRESUPUESTO

Registrar por:

```text
proyecto
+
vigencia
+
fuente
```

Campos:

- apropiación inicial;
- adiciones;
- reducciones;
- apropiación definitiva.

---

## 36. EJECUCIÓN FINANCIERA

Registrar:

- CDP;
- RP/compromisos;
- obligaciones;
- pagos;
- porcentaje.

---

## 37. CRUCE FÍSICO-FINANCIERO

Crear motor:

```text
AVANCE FÍSICO
VS
AVANCE FINANCIERO
```

Calcular desviación.

Umbrales configurables.

---

## 38. CONTRATOS

SIGM NO reemplaza SECOP.

Crear seguimiento interno.

Registrar:

- número;
- SECOP ID;
- objeto;
- contratista;
- supervisor;
- fechas;
- valor;
- avance;
- estado.

---

## 39. CONTRATO ↔ META

N:M mediante:

```text
contrato_meta
```

---

## 40. EVIDENCIAS

PostgreSQL guarda:

- metadatos;
- SHA-256;
- clasificación;
- versión.

Objeto en storage privado.

---

## 41. CLASIFICACIÓN DOCUMENTAL

Estados:

```text
PUBLICA
CLASIFICADA
RESERVADA
INTERNA
```

No asumir automáticamente que un archivo es público.

---

## 42. ALERTAS

Crear motor de alertas.

Tipos iniciales:

```text
META_ATRASADA
SIN_REPORTE
DESVIACION_FISICO_FINANCIERA
PROYECTO_ATRASADO
CONTRATO_PROXIMO_VENCER
ACTIVIDAD_VENCIDA
```

---

## 43. SNAPSHOTS

Los cortes oficiales deberán congelarse.

Tabla:

```text
snapshots_reporte
```

Un snapshot aprobado es inmutable.

---

## 44. AUDITORÍA

Implementar:

```text
audit_events
```

append-only.

Registrar:

```text
QUIÉN
QUÉ
CUÁNDO
ANTES
DESPUÉS
IP
TENANT
CORRELATION_ID
```

---

## 45. DASHBOARD DEL ALCALDE

Mostrar:

- avance global PDT;
- ejecución financiera;
- metas totales;
- metas cumplidas;
- metas críticas;
- metas sin reporte;
- desviaciones físico-financieras;
- proyectos activos;
- proyectos atrasados;
- contratos;
- alertas críticas;
- avance por secretaría;
- avance por sector;
- tendencia cuatrienal.

---

## 46. DRILL-DOWN

Debe permitir:

```text
ALCALDÍA
→ SECRETARÍA
→ PROGRAMA
→ META
→ PROYECTO
→ PRESUPUESTO
→ CONTRATO
→ EVIDENCIA
```

---

## 47. TRAZABILIDAD DE META

Endpoint prioritario:

```text
GET /api/v1/metas/{id}/trazabilidad
```

Debe consolidar:

- Plan;
- nodo;
- indicador;
- programación;
- avances;
- proyectos;
- presupuesto;
- ejecución;
- contratos;
- evidencias;
- alertas.

---

## 48. DASHBOARD BACKEND

Endpoint:

```text
GET /api/v1/dashboard/alcalde
```

Evitar múltiples consultas innecesarias.

---

## 49. REPORTES

Implementar:

- seguimiento PDT;
- metas;
- indicadores;
- dependencia;
- proyectos;
- físico-financiero;
- resumen gerencial.

Exportaciones:

- PDF;
- Excel.

---

## 50. MATRIZ LEGAL

Crear módulo/catálogo inicial.

Estructura:

```text
Norma
Artículo
Requisito
Proceso
Módulo
Funcionalidad
Evidencia
Responsable
Estado
Fuente oficial
Vigencia
```

No quemar legislación en lógica rígida.

---

## 51. MARCO LEGAL BASE

Incluir inicialmente:

- Constitución Política.
- Ley 152 de 1994.
- Ley 87 de 1993.
- Ley 489 de 1998.
- Decreto 1083 de 2015.
- Decreto 1499 de 2017.
- Ley 1712 de 2014.
- Ley 1757 de 2015.
- Ley 1474 de 2011.
- Ley 2195 de 2022.
- Ley 80 de 1993.
- Ley 1150 de 2007.
- Decreto 1082 de 2015.
- Decreto 111 de 1996.
- Ley 594 de 2000.
- Ley 1581 de 2012.
- Ley 2052 de 2020.
- Ley 909 de 2004.

Validar vigencia antes de crear automatizaciones basadas en artículos.

---

## 52. INTEGRACIONES

Crear capa:

```text
integrations/
```

No acoplar núcleo directamente.

Interfaces futuras:

```text
SisPTAdapter
FinancialSystemAdapter
SecopAdapter
PIIPAdapter
CUIPOAdapter
FURAGAdapter
```

---

## 53. SisPT

Prioridad alta.

NO inventar API.

Permitir:

- importación;
- exportación;
- conciliación.

---

## 54. SISTEMA FINANCIERO

Prioridad alta.

SIGM debe importar datos financieros para evitar doble digitación.

Crear importación CSV/XLSX como mecanismo inicial si no existe API.

---

## 55. SECOP

Guardar referencias.

Integración solamente mediante mecanismos oficiales existentes.

---

## 56. FRONTEND

Diseñar una interfaz institucional profesional.

Características:

- responsive;
- accesible;
- menú lateral;
- breadcrumbs;
- tablas;
- filtros;
- cards;
- gráficos;
- estados;
- drill-down.

---

## 57. MENÚ PRINCIPAL V1

```text
Dashboard

Planeación
 ├ Plan de Desarrollo
 ├ Indicadores
 ├ Metas
 ├ Plan Indicativo
 └ Planes de Acción

Ejecución
 ├ Proyectos
 ├ Presupuesto
 ├ Seguimiento financiero
 └ Contratos

Seguimiento
 ├ Avances
 ├ Alertas
 └ Evidencias

Reportes

Administración
 ├ Entidad
 ├ Dependencias
 ├ Usuarios
 ├ Roles
 └ Configuración

Auditoría
```

---

## 58. UX

Toda pantalla debe tener:

- título;
- descripción breve;
- filtros;
- búsqueda;
- acciones;
- permisos;
- estados;
- paginación;
- loading;
- empty state;
- errores.

---

## 59. ACCESIBILIDAD

Aplicar WCAG cuando sea viable.

No depender solo del color.

---

## 60. SEGURIDAD

Aplicar:

- JWT;
- MFA preparado;
- RBAC;
- multitenancy;
- RLS;
- IDOR protection;
- rate limiting;
- validación;
- CORS;
- TLS;
- secret management;
- auditoría;
- headers seguros.

---

## 61. PROTECCIÓN DE DATOS

Aplicar principios de:

- minimización;
- necesidad;
- clasificación;
- acceso restringido;
- trazabilidad.

---

## 62. LOGS

No registrar:

- contraseñas;
- tokens;
- secretos;
- documentos;
- datos personales innecesarios.

---

## 63. CORRELATION ID

Cada request crítico tendrá:

```text
correlation_id UUID
```

---

## 64. ERRORES

Formato:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "No se encontró el recurso solicitado",
    "correlation_id": "..."
  }
}
```

---

## 65. OPENAPI

Todos los endpoints deben estar documentados.

---

## 66. PAGINACIÓN

Aplicar:

```text
page
page_size
sort
filters
search
```

---

## 67. IMPORTADORES

Crear importadores controlados para:

- Plan de Desarrollo;
- metas;
- indicadores;
- presupuesto.

Permitir previsualización antes de confirmar.

---

## 68. VALIDACIÓN DE IMPORTACIÓN

Flujo:

```text
ARCHIVO
→ PARSEO
→ VALIDACIÓN
→ PREVISUALIZACIÓN
→ ERRORES
→ CONFIRMACIÓN
→ TRANSACCIÓN
→ AUDITORÍA
```

---

## 69. TESTING

Crear:

- Unit tests
- Integration tests
- API tests
- Multitenancy tests
- Security tests
- Migration tests
- Frontend component tests
- E2E tests

---

## 70. ESCENARIO DEMO

Crear tenant:

```text
Alcaldía Demo
```

Plan:

```text
Municipio Avanza 2024-2027
```

Meta:

```text
Construir 20 km de vías
```

Proyecto:

```text
Mejoramiento vial urbano
```

Presupuesto:

```text
10.000.000.000 COP
```

Contrato:

```text
CT-001-2026
```

Avance físico:

```text
45 %
```

Avance financiero:

```text
75 %
```

El sistema deberá generar alerta de desviación.

---

## 71. DATOS DEMO

Nunca poner datos demo en migraciones.

Usar:

```text
scripts/seeds/demo
```

---

## 72. DOCKER

Crear:

```text
Dockerfile backend
Dockerfile frontend
docker-compose.dev.yml
docker-compose.prod.yml
```

Servicios:

```text
postgres
backend
frontend
redis opcional
minio opcional
reverse-proxy
```

---

## 73. ENTORNOS

Separar:

```text
development
testing
staging
production
```

---

## 74. VARIABLES

Crear:

```text
.env.example
```

Nunca subir `.env` real.

---

## 75. CI/CD

Pipeline mínimo:

```text
lint
↓
tests
↓
migration test
↓
build
↓
security checks
```

---

## 76. QUALITY GATES

No permitir merge si fallan:

- tests;
- lint;
- migraciones;
- type checks;
- build.

---

## 77. HEALTH CHECKS

Crear:

```text
/health
/ready
```

---

## 78. BACKUPS

Diseñar:

- backups PostgreSQL;
- backup de storage;
- retención;
- restauración probada.

---

## 79. OBSERVABILIDAD

- Logs estructurados.
- Métricas.
- Errores.
- Health.
- Performance.

---

## 80. FASES DEL PROYECTO

### FASE 0 – DESCUBRIMIENTO

Si repositorio vacío:

definir estructura base.

Si existe proyecto:

auditarlo.

Entregar:

- stack;
- estructura;
- brechas;
- riesgos.

### FASE 1 – FOUNDATION

Crear:

- repositorio;
- backend;
- frontend;
- PostgreSQL;
- Docker;
- configuración;
- CI/CD;
- estándares.

### FASE 2 – SEGURIDAD Y MULTITENANCY

Crear:

- tenants;
- auth;
- usuarios;
- RBAC;
- tenant context;
- tests aislamiento.

### FASE 3 – NÚCLEO INSTITUCIONAL

Crear:

- municipio;
- administración;
- dependencias;
- configuración.

### FASE 4 – PLAN DE DESARROLLO

Crear:

- plan;
- versiones;
- jerarquía;
- nodos.

### FASE 5 – INDICADORES Y METAS

Crear:

- indicadores;
- metas;
- fichas técnicas.

### FASE 6 – PLAN INDICATIVO

Crear:

- programación anual;
- acumulados;
- validaciones.

### FASE 7 – PLANES DE ACCIÓN

Crear:

- plan;
- actividades;
- responsables;
- avance.

### FASE 8 – PROYECTOS

Crear:

- proyectos;
- proyecto-meta;
- BPIN;
- estados.

### FASE 9 – SEGUIMIENTO FÍSICO

Crear:

- avances;
- workflow;
- validación;
- aprobación.

### FASE 10 – PRESUPUESTO

Crear:

- presupuesto;
- fuentes;
- importador;
- ejecución.

### FASE 11 – CONTRATOS

Crear:

- seguimiento contractual;
- contrato-meta;
- supervisor.

### FASE 12 – MOTOR FÍSICO-FINANCIERO

Crear:

- comparación;
- reglas;
- severidad;
- alertas.

### FASE 13 – EVIDENCIAS

Crear:

- upload;
- metadata;
- hash;
- storage;
- permisos.

### FASE 14 – SNAPSHOTS

Crear:

- cierres;
- hashes;
- inmutabilidad.

### FASE 15 – DASHBOARD

Crear:

- dashboard Alcalde;
- dashboard Secretaría;
- drill-down.

### FASE 16 – REPORTES

Crear:

- PDF;
- Excel;
- seguimiento;
- gerencial.

### FASE 17 – MATRIZ LEGAL

Crear:

- catálogo;
- requisitos;
- evidencias;
- vigencia.

### FASE 18 – AUDITORÍA

Completar:

- eventos;
- before/after;
- correlación;
- consultas.

### FASE 19 – INTEGRACIONES

Crear adapters.

Implementar solo integraciones verificadas.

### FASE 20 – HARDENING

Ejecutar:

- seguridad;
- IDOR;
- RLS;
- rate limit;
- pruebas aislamiento;
- permisos.

### FASE 21 – QA COMPLETO

Ejecutar:

- backend;
- frontend;
- DB;
- migraciones;
- E2E.

### FASE 22 – PILOTO

Crear Alcaldía piloto.

Cargar PDT.

Medir calidad.

### FASE 23 – STAGING

Prueba preproducción.

### FASE 24 – PRODUCCIÓN V1

Deploy controlado.

---

## 81. ORDEN ESTRICTO

NO desarrollar simultáneamente todo.

Prioridad:

```text
NÚCLEO
→ PDT
→ INDICADORES
→ METAS
→ PLAN INDICATIVO
→ PLANES DE ACCIÓN
→ PROYECTOS
→ SEGUIMIENTO
→ PRESUPUESTO
→ DASHBOARD
```

---

## 82. CRITERIOS DE ACEPTACIÓN PRINCIPALES

V1 se considera completa si:

1. Puede operar múltiples Alcaldías aisladas.
2. Puede crear un PDT completo.
3. Puede crear una jerarquía configurable.
4. Puede crear metas e indicadores.
5. Puede programar metas por vigencia.
6. Puede registrar avances.
7. Puede aprobar avances.
8. Puede crear Planes de Acción.
9. Puede crear proyectos.
10. Proyecto puede soportar varias metas.
11. Puede registrar presupuesto.
12. Puede importar ejecución financiera.
13. Puede relacionar contratos.
14. Puede cargar evidencias.
15. Puede calcular físico-financiero.
16. Puede generar alertas.
17. Puede congelar snapshots.
18. El Alcalde puede navegar hasta evidencia.
19. Los reportes aprobados no cambian.
20. Auditoría registra operaciones críticas.
21. Tenant A jamás accede a Tenant B.
22. OpenAPI está documentado.
23. Tests pasan.
24. Migraciones son reproducibles.
25. Docker permite despliegue.

---

## 83. MÉTRICAS DEL PILOTO

Medir:

- % PDT cargado;
- % metas válidas;
- % metas con indicador;
- % metas con responsable;
- % reportes a tiempo;
- % evidencias trazables;
- reducción de Excel;
- reducción de tiempo de consolidación;
- metas críticas identificadas;
- uso por secretarías;
- uso Alcalde;
- errores de calidad;
- incidentes de seguridad.

Objetivo:

```text
0 accesos cross-tenant
```

---

## 84. DEFINICIÓN DE DONE

Una funcionalidad NO está terminada solo porque “funciona en mi máquina”.

Debe tener, cuando corresponda:

```text
DB
+
migration
+
model
+
schema
+
service
+
API
+
frontend
+
permissions
+
audit
+
tests
+
documentation
```

---

## 85. REGLA DE MIGRACIONES

No modificar migraciones ya ejecutadas.

Agregar nueva migración.

---

## 86. REGLA DE SEGURIDAD

Nunca sacrificar aislamiento multitenant por facilidad de desarrollo.

---

## 87. REGLA DE DATOS

Nunca duplicar:

- meta;
- indicador;
- proyecto;
- contrato.

Fuente única.

---

## 88. REGLA DE HISTÓRICO

Nunca sobrescribir silenciosamente datos aprobados.

---

## 89. REGLA DE INTEGRACIONES

Nunca inventar APIs.

---

## 90. REGLA LEGAL

Nunca afirmar automáticamente:

> “Cumple la ley”

solo porque existe una pantalla.

La plataforma:

- soporta;
- evidencia;
- facilita;
- controla;

pero el cumplimiento institucional requiere gestión real.

---

## 91. REGLA DE CAMBIO

Todo cambio al contrato debe registrar:

```text
ADR
```

Guardar en:

```text
docs/adr/
```

---

## 92. DOCUMENTACIÓN

Crear:

```text
README.md
ARCHITECTURE.md
SECURITY.md
DATABASE.md
API.md
DEPLOYMENT.md
CONTRIBUTING.md
CHANGELOG.md
```

---

## 93. DOCUMENTACIÓN PARA USUARIO

Crear manuales:

- Administrador.
- Planeación.
- Secretario.
- Responsable de proyecto.
- Alcalde.
- Control Interno.

---

## 94. NO HACER

NO:

- comenzar por frontend sin backend;
- comenzar por dashboard sin fuente de datos;
- duplicar tablas;
- quemar legislación;
- usar eval;
- usar float en dinero;
- permitir cross-tenant;
- usar cascade delete en históricos;
- guardar archivos sensibles públicos;
- alterar snapshots;
- eliminar auditoría;
- inventar integraciones;
- implementar contabilidad completa en V1;
- implementar nómina completa en V1;
- reemplazar SECOP;
- reemplazar SisPT.

---

## 95. ENTREGABLE POR FASE

Al finalizar cada fase entregar:

### RESUMEN
Qué se hizo.

### ARCHIVOS
Creados/modificados.

### BASE DE DATOS
Tablas/migraciones.

### API
Endpoints.

### FRONTEND
Pantallas/componentes.

### SEGURIDAD
Controles.

### PRUEBAS
Tests ejecutados.

### RESULTADO
Pass/fail.

### PENDIENTES
Qué falta.

### DEUDA TÉCNICA
Si existe.

### ADR
Decisiones importantes.

---

## 96. NO AVANZAR CON ERRORES

Antes de iniciar siguiente fase:

- tests actuales pasan;
- migraciones funcionan;
- aplicación inicia;
- build frontend pasa;
- no hay error crítico conocido.

---

## 97. FLUJO DE DESARROLLO

Cada fase:

```text
ANALIZAR
↓
DISEÑAR
↓
IMPLEMENTAR
↓
MIGRAR
↓
PROBAR
↓
AUDITAR
↓
DOCUMENTAR
↓
VALIDAR
```

---

## 98. RESULTADO FINAL ESPERADO

Al finalizar el proyecto debe existir:

# SIGM COLOMBIA V1

con:

```text
Frontend operativo
+
Backend FastAPI
+
PostgreSQL
+
Alembic
+
SQLAlchemy
+
Multitenancy
+
RBAC
+
Plan de Desarrollo
+
Indicadores
+
Metas
+
Plan Indicativo
+
Planes de Acción
+
Proyectos
+
Presupuesto
+
Contratos
+
Seguimiento físico
+
Seguimiento financiero
+
Alertas
+
Evidencias
+
Snapshots
+
Dashboard
+
Reportes
+
Matriz legal
+
Auditoría
+
Docker
+
CI/CD
+
Tests
+
Documentación
```

---

## 99. CONSULTA ESTRATÉGICA FINAL

El sistema debe poder responder:

```text
¿Cuál es el avance de esta meta?
```

y mostrar:

```text
Plan
→ Programa
→ Meta
→ Indicador
→ Programación
→ Ejecución física
→ Proyecto
→ Presupuesto
→ Ejecución financiera
→ Contratos
→ Evidencias
→ Alertas
→ Responsable
→ Histórico
```

---

## 100. INSTRUCCIÓN DE ARRANQUE AL AGENTE

NO EMPIECES PROGRAMANDO.

Primero:

### PASO 1

Lee completos:

- `docs/01_ALCANCE_ARQUITECTURA_V1.md`
- `docs/02_ER_DICCIONARIO_DATOS_V1.md`
- este archivo `docs/03_PROMPT_MAESTRO_DESARROLLO_SIGM_V1.md`

### PASO 2

Audita el repositorio actual.

### PASO 3

Entrega:

1. Estado actual.
2. Stack encontrado.
3. Arquitectura encontrada.
4. Mapa de carpetas.
5. Base de datos existente.
6. Modelos existentes.
7. Migraciones existentes.
8. Seguridad existente.
9. Autenticación existente.
10. Multitenancy existente.
11. Frontend existente.
12. Componentes reutilizables.
13. Conflictos con los documentos contractuales.
14. Elementos faltantes.
15. Riesgos.
16. Arquitectura final propuesta.
17. Estructura de repositorio.
18. Plan de implementación por fases.
19. Matriz contrato → implementación.

### PASO 4

Después de esta auditoría:

# INICIA FASE 1.

Continúa secuencialmente hasta completar la V1.

No preguntes nuevamente por requisitos que estén definidos en los documentos contractuales.

Cuando exista una decisión técnica menor no definida, aplica la alternativa más segura, mantenible y compatible con los contratos, documentándola en ADR.

---

# PRINCIPIO MAESTRO

EL DOCUMENTO DE ALCANCE DEFINE QUÉ CONSTRUIR.

EL DICCIONARIO DE DATOS DEFINE CÓMO PERSISTIRLO.

EL PLAN DE DESARROLLO ES EL CEREBRO FUNCIONAL.

POSTGRESQL ES LA FUENTE DE VERDAD.

FASTAPI ES LA CAPA DE SERVICIOS.

EL FRONTEND ES LA INTERFAZ DE GESTIÓN.

MULTITENANCY GARANTIZA EL AISLAMIENTO.

AUDITORÍA GARANTIZA LA TRAZABILIDAD.

SNAPSHOTS GARANTIZAN EL HISTÓRICO.

LAS EVIDENCIAS RESPALDAN LOS RESULTADOS.

Y LA CADENA:

# PLAN → META → PROYECTO → PRESUPUESTO → CONTRATO → RESULTADO

ES EL CORAZÓN DE SIGM COLOMBIA.
