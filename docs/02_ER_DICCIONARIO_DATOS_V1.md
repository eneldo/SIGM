**SIGM COLOMBIA**

**Documento Maestro - Diagrama ER + Diccionario de Datos del Núcleo Central V1**

*Sistema Integral de Gestión Municipal*

| **Documento**                  | Documento Maestro ER + Diccionario de Datos         |
|--------------------------------|-----------------------------------------------------|
| **Versión**                    | 1.0                                                 |
| **Alcance**                    | Núcleo Central V1                                   |
| **Plataforma**                 | SIGM Colombia                                       |
| **Motor de datos recomendado** | PostgreSQL 17+                                      |
| **Arquitectura**               | Modular, API-first, multi-tenant, auditable         |
| **Estado**                     | Base técnica para diseño físico, migraciones y APIs |

# Contenido

1.  1\. Propósito y alcance

2.  2\. Principios de diseño de datos

3.  3\. Núcleo Central V1

4.  4\. Diagrama Entidad-Relación

5.  5\. Convenciones y estándares

6.  6\. Relaciones y cardinalidades

7.  7\. Diccionario de datos

8.  8\. Reglas de integridad y negocio

9.  9\. Multitenancy y seguridad de datos

10. 10\. Auditoría y trazabilidad

11. 11\. Índices y rendimiento

12. 12\. Estrategia de versionamiento y snapshots

13. 13\. Orden de implementación

14. 14\. Criterios de aceptación del modelo

15. 15\. Decisiones arquitectónicas abiertas

# 1. Propósito y alcance

Este documento define el modelo lógico inicial del Núcleo Central V1 de SIGM Colombia. Su objetivo es transformar el alcance funcional aprobado en una estructura de datos coherente, auditable y preparada para PostgreSQL, de modo que sirva como fuente para migraciones, modelos ORM, servicios, APIs, pruebas y reportes.

- Modela la estructura institucional y el aislamiento por Alcaldía/tenant.

- Modela el Plan de Desarrollo Municipal como eje estratégico.

- Conecta metas, indicadores, Plan Indicativo, Planes de Acción, proyectos, presupuesto, contratos y avances.

- Incluye evidencias, alertas, snapshots e historial de auditoría.

- No incluye todavía contabilidad, tesorería, nómina, PQRSD, MIPG completo ni gestión documental archivística completa; quedan como módulos posteriores o integraciones.

# 2. Principios de diseño de datos

- Fuente única de verdad: una meta, proyecto, indicador o contrato no debe duplicarse entre módulos.

- Trazabilidad bidireccional: desde una meta se debe llegar a proyecto, presupuesto, contrato, avance y evidencia; y viceversa.

- Multitenancy desde el origen: toda entidad sensible debe pertenecer inequívocamente a un tenant.

- Histórico preservado: los informes aprobados y cortes oficiales no deben cambiar por modificaciones posteriores.

- Auditoría por diseño: las operaciones críticas deben dejar rastro de quién, qué, cuándo, antes y después.

- Catálogos parametrizables: estados, tipos de nivel, periodicidades y unidades no deben quedar rígidos en el frontend.

- Integración primero: presupuesto/contratación pueden provenir de sistemas externos sin romper el modelo central.

- Integridad referencial: preferir FK reales y restricciones SQL sobre validaciones exclusivamente de aplicación.

# 3. Núcleo Central V1

El núcleo funcional se organiza en cinco dominios:

| **Dominio**           | **Responsabilidad**                                                                          |
|-----------------------|----------------------------------------------------------------------------------------------|
| Institucional         | Tenant, municipio, administración, dependencias, usuarios y roles.                           |
| Planeación            | Plan de Desarrollo, estructura jerárquica, metas, indicadores, programación anual y avances. |
| Ejecución             | Planes de Acción, actividades, proyectos, presupuesto y contratos.                           |
| Control gerencial     | Alertas, cortes, snapshots y reglas de desviación físico-financiera.                         |
| Evidencia y auditoría | Archivos/evidencias, bitácora y trazabilidad transversal.                                    |

# 4. Diagrama Entidad-Relación

El siguiente diagrama representa el modelo lógico recomendado para la V1. Las entidades asociativas permiten relaciones N:M sin duplicar información.

<img src="/mnt/data/SIGM_MD/media_er/media/image1.png" style="width:9.7in;height:1.52215in" />

*Figura 1. Diagrama ER lógico del Núcleo Central V1.*

# 5. Convenciones y estándares

| **Elemento**    | **Convención**                                                                      |
|-----------------|-------------------------------------------------------------------------------------|
| Nombres físicos | snake_case en español o inglés consistente; este documento usa español descriptivo. |
| PK              | UUID (uuid) generado en backend o gen_random_uuid().                                |
| FK              | \<entidad\>\_id, tipo UUID.                                                         |
| Fechas          | timestamptz para eventos; date para vigencias/fechas de negocio.                    |
| Dinero          | numeric(18,2).                                                                      |
| Porcentajes     | numeric(7,4) o derivados, nunca float.                                              |
| Soft delete     | deleted_at cuando la eliminación lógica sea necesaria.                              |
| Auditoría común | created_at, created_by, updated_at, updated_by.                                     |
| Tenant          | tenant_id obligatorio en toda tabla de negocio susceptible de aislamiento.          |
| Estados         | varchar/catálogo o enum controlado; evitar texto libre.                             |
| JSON            | jsonb solo para metadatos flexibles, snapshots o payloads no relacionales.          |

# 6. Relaciones y cardinalidades

| **Origen**          | **Relación**  | **Destino**            | **Regla**                                                           |
|---------------------|---------------|------------------------|---------------------------------------------------------------------|
| Tenant              | 1:N           | Municipio              | Un tenant representa una entidad/instancia administrativa.          |
| Municipio           | 1:N           | Administración         | Permite conservar periodos de gobierno históricos.                  |
| Tenant              | 1:N           | Dependencia            | La estructura orgánica queda aislada por entidad.                   |
| Dependencia         | 1:N recursiva | Dependencia            | Jerarquía despacho/secretaría/dirección/oficina.                    |
| Administración      | 1:N           | Plan de Desarrollo     | Permite versiones o planes por periodo.                             |
| Plan de Desarrollo  | 1:N           | Nodo de Plan           | Jerarquía flexible: línea, sector, programa, producto u otro nivel. |
| Nodo de Plan        | 1:N           | Meta                   | Las metas se asocian al nivel estratégico pertinente.               |
| Indicador           | 1:N           | Meta                   | Un indicador puede medir una o varias metas cuando sea válido.      |
| Meta                | 1:N           | Programación anual     | Plan Indicativo por vigencia.                                       |
| Meta                | 1:N           | Avance                 | Cortes periódicos físicos.                                          |
| Plan de Acción      | 1:N           | Actividad              | Actividades operativas por dependencia.                             |
| Actividad           | N:1           | Meta                   | Toda actividad V1 debe contribuir a una meta.                       |
| Proyecto            | N:M           | Meta                   | Mediante proyecto_meta.                                             |
| Proyecto            | 1:N           | Presupuesto            | Apropiaciones por vigencia/fuente.                                  |
| Presupuesto         | 1:N           | Ejecución presupuestal | Cortes de compromisos, obligaciones y pagos.                        |
| Proyecto            | 1:N           | Contrato               | Seguimiento interno contractual.                                    |
| Contrato            | N:M           | Meta                   | Mediante contrato_meta.                                             |
| Entidad transversal | 1:N           | Evidencia              | Asociación polimórfica controlada.                                  |
| Entidad transversal | 1:N           | Alerta                 | Alertas sobre metas, proyectos, contratos, etc.                     |

# 7. Diccionario de datos

Las tablas siguientes representan el mínimo recomendado para el núcleo. En implementación física pueden separarse por schemas (core, planning, execution, audit) sin cambiar las relaciones conceptuales.

## 7.1 tenants

Raíz de aislamiento lógico de cada Alcaldía o entidad territorial.

| **Campo**     | **Tipo**     | **Clave/Regla** | **Nulo** | **Descripción**              |
|---------------|--------------|-----------------|----------|------------------------------|
| id            | uuid         | PK              | Sí       | Identificador.               |
| nombre        | varchar(180) |                 | Sí       | Nombre del tenant.           |
| slug          | varchar(80)  | UNIQUE          | Sí       | Identificador amigable.      |
| nit           | varchar(30)  |                 | No       | NIT de la entidad.           |
| estado        | varchar(20)  |                 | Sí       | ACTIVO/INACTIVO/SUSPENDIDO.  |
| configuracion | jsonb        |                 | No       | Parámetros no estructurales. |

**Restricciones principales:** slug único global.

**Índices sugeridos:** unique(slug), index(estado)

## 7.2 municipios

Datos de identificación territorial.

| **Campo**    | **Tipo**     | **Clave/Regla** | **Nulo** | **Descripción**              |
|--------------|--------------|-----------------|----------|------------------------------|
| id           | uuid         | PK              | Sí       | Identificador.               |
| tenant_id    | uuid         | FK tenants.id   | Sí       | Tenant.                      |
| codigo_dane  | varchar(5)   |                 | Sí       | Código DANE del municipio.   |
| nombre       | varchar(160) |                 | Sí       | Nombre oficial.              |
| departamento | varchar(120) |                 | Sí       | Departamento.                |
| categoria    | varchar(30)  |                 | No       | Categoría municipal vigente. |
| nit          | varchar(30)  |                 | No       | NIT.                         |
| sitio_web    | varchar(255) |                 | No       | URL institucional.           |
| logo_uri     | varchar(500) |                 | No       | Ubicación de logo/escudo.    |

**Restricciones principales:** unique(tenant_id, codigo_dane).

**Índices sugeridos:** index(tenant_id), index(codigo_dane)

## 7.3 administraciones

Periodos constitucionales o administrativos de gobierno.

| **Campo**      | **Tipo**     | **Clave/Regla**  | **Nulo** | **Descripción**                |
|----------------|--------------|------------------|----------|--------------------------------|
| id             | uuid         | PK               | Sí       | Identificador.                 |
| tenant_id      | uuid         | FK tenants.id    | Sí       | Tenant.                        |
| municipio_id   | uuid         | FK municipios.id | Sí       | Municipio.                     |
| nombre         | varchar(180) |                  | No       | Nombre/lema de administración. |
| alcalde_nombre | varchar(180) |                  | Sí       | Nombre del alcalde.            |
| periodo_inicio | date         |                  | Sí       | Inicio.                        |
| periodo_fin    | date         |                  | Sí       | Fin.                           |
| estado         | varchar(20)  |                  | Sí       | PLANEADA/ACTIVA/CERRADA.       |

**Restricciones principales:** periodo_fin \>= periodo_inicio.

**Índices sugeridos:** index(tenant_id, estado), index(municipio_id, periodo_inicio)

## 7.4 dependencias

Estructura orgánica de la Alcaldía.

| **Campo**              | **Tipo**     | **Clave/Regla**    | **Nulo** | **Descripción**                            |
|------------------------|--------------|--------------------|----------|--------------------------------------------|
| id                     | uuid         | PK                 | Sí       | Identificador.                             |
| tenant_id              | uuid         | FK tenants.id      | Sí       | Tenant.                                    |
| parent_id              | uuid         | FK dependencias.id | No       | Dependencia superior.                      |
| codigo                 | varchar(40)  |                    | No       | Código interno.                            |
| nombre                 | varchar(180) |                    | Sí       | Nombre.                                    |
| tipo                   | varchar(40)  |                    | Sí       | DESPACHO/SECRETARIA/OFICINA/DIRECCION/etc. |
| responsable_usuario_id | uuid         | FK usuarios.id     | No       | Responsable vigente.                       |
| estado                 | varchar(20)  |                    | Sí       | ACTIVA/INACTIVA.                           |

**Restricciones principales:** No permitir ciclos jerárquicos. \| unique(tenant_id,codigo) cuando código no sea nulo.

**Índices sugeridos:** index(tenant_id,parent_id), index(tenant_id,estado)

## 7.5 usuarios

Identidad de usuarios internos.

| **Campo**       | **Tipo**     | **Clave/Regla**    | **Nulo** | **Descripción**            |
|-----------------|--------------|--------------------|----------|----------------------------|
| id              | uuid         | PK                 | Sí       | Identificador.             |
| tenant_id       | uuid         | FK tenants.id      | Sí       | Tenant.                    |
| dependencia_id  | uuid         | FK dependencias.id | No       | Dependencia principal.     |
| nombre_completo | varchar(180) |                    | Sí       | Nombre.                    |
| email           | citext       |                    | Sí       | Correo.                    |
| password_hash   | varchar(255) |                    | Sí       | Hash, nunca texto plano.   |
| estado          | varchar(20)  |                    | Sí       | ACTIVO/BLOQUEADO/INACTIVO. |
| ultimo_acceso   | timestamptz  |                    | No       | Último acceso exitoso.     |

**Restricciones principales:** unique(tenant_id,email).

**Índices sugeridos:** index(tenant_id,email), index(dependencia_id)

## 7.6 roles

Roles RBAC.

| **Campo**   | **Tipo**    | **Clave/Regla** | **Nulo** | **Descripción**                   |
|-------------|-------------|-----------------|----------|-----------------------------------|
| id          | uuid        | PK              | Sí       | Identificador.                    |
| tenant_id   | uuid        | FK tenants.id   | No       | Nulo si rol global de plataforma. |
| nombre      | varchar(80) |                 | Sí       | Nombre.                           |
| descripcion | text        |                 | No       | Descripción.                      |
| es_sistema  | boolean     |                 | Sí       | Protege roles base.               |

**Restricciones principales:** unique(tenant_id,nombre).

**Índices sugeridos:** index(tenant_id,nombre)

## 7.7 usuario_roles

Tabla puente usuarios-roles.

| **Campo**   | **Tipo**    | **Clave/Regla** | **Nulo** | **Descripción**      |
|-------------|-------------|-----------------|----------|----------------------|
| usuario_id  | uuid        | FK usuarios.id  | Sí       | Usuario.             |
| rol_id      | uuid        | FK roles.id     | Sí       | Rol.                 |
| asignado_at | timestamptz |                 | Sí       | Fecha de asignación. |
| asignado_by | uuid        | FK usuarios.id  | No       | Quién asigna.        |

**Restricciones principales:** PK compuesta(usuario_id,rol_id).

**Índices sugeridos:** index(rol_id)

## 7.8 planes_desarrollo

Cabecera del Plan de Desarrollo Municipal.

| **Campo**         | **Tipo**     | **Clave/Regla**        | **Nulo** | **Descripción**                         |
|-------------------|--------------|------------------------|----------|-----------------------------------------|
| id                | uuid         | PK                     | Sí       | Identificador.                          |
| tenant_id         | uuid         | FK tenants.id          | Sí       | Tenant.                                 |
| administracion_id | uuid         | FK administraciones.id | Sí       | Periodo de gobierno.                    |
| nombre            | varchar(220) |                        | Sí       | Nombre oficial.                         |
| acuerdo_numero    | varchar(80)  |                        | No       | Acto de aprobación.                     |
| fecha_aprobacion  | date         |                        | No       | Fecha.                                  |
| vigencia_inicio   | smallint     |                        | Sí       | Año inicial.                            |
| vigencia_fin      | smallint     |                        | Sí       | Año final.                              |
| version           | integer      |                        | Sí       | Versión lógica.                         |
| estado            | varchar(25)  |                        | Sí       | FORMULACION/APROBADO/EJECUCION/CERRADO. |

**Restricciones principales:** vigencia_fin \>= vigencia_inicio. \| No más de un plan ACTIVO por administración salvo versión explícita.

**Índices sugeridos:** index(tenant_id,estado), unique(administracion_id,version)

## 7.9 nodos_plan

Jerarquía flexible del PDT.

| **Campo** | **Tipo**     | **Clave/Regla**         | **Nulo** | **Descripción**                           |
|-----------|--------------|-------------------------|----------|-------------------------------------------|
| id        | uuid         | PK                      | Sí       | Identificador.                            |
| tenant_id | uuid         | FK tenants.id           | Sí       | Tenant.                                   |
| plan_id   | uuid         | FK planes_desarrollo.id | Sí       | Plan.                                     |
| parent_id | uuid         | FK nodos_plan.id        | No       | Nodo superior.                            |
| tipo      | varchar(40)  |                         | Sí       | PILAR/LINEA/SECTOR/PROGRAMA/PRODUCTO/etc. |
| codigo    | varchar(80)  |                         | Sí       | Código interno/oficial.                   |
| nombre    | varchar(300) |                         | Sí       | Nombre.                                   |
| orden     | integer      |                         | Sí       | Orden visual.                             |
| estado    | varchar(20)  |                         | Sí       | ACTIVO/INACTIVO.                          |

**Restricciones principales:** No permitir ciclos. \| unique(plan_id,codigo).

**Índices sugeridos:** index(plan_id,parent_id), index(plan_id,tipo)

## 7.10 indicadores

Catálogo de indicadores de planeación.

| **Campo**                  | **Tipo**     | **Clave/Regla**    | **Nulo** | **Descripción**                     |
|----------------------------|--------------|--------------------|----------|-------------------------------------|
| id                         | uuid         | PK                 | Sí       | Identificador.                      |
| tenant_id                  | uuid         | FK tenants.id      | Sí       | Tenant.                             |
| codigo                     | varchar(80)  |                    | Sí       | Código.                             |
| nombre                     | varchar(250) |                    | Sí       | Nombre.                             |
| descripcion                | text         |                    | No       | Definición.                         |
| tipo                       | varchar(30)  |                    | Sí       | PRODUCTO/RESULTADO/GESTION/etc.     |
| unidad_medida              | varchar(60)  |                    | Sí       | Unidad.                             |
| sentido                    | varchar(20)  |                    | Sí       | ASCENDENTE/DESCENDENTE/MANTENER.    |
| formula                    | text         |                    | No       | Expresión descriptiva/controlada.   |
| fuente                     | varchar(250) |                    | No       | Fuente de datos.                    |
| periodicidad               | varchar(30)  |                    | Sí       | MENSUAL/TRIMESTRAL/SEMESTRAL/ANUAL. |
| responsable_dependencia_id | uuid         | FK dependencias.id | No       | Responsable.                        |

**Restricciones principales:** unique(tenant_id,codigo).

**Índices sugeridos:** index(tenant_id,tipo), index(responsable_dependencia_id)

## 7.11 metas

Meta física del Plan de Desarrollo.

| **Campo**       | **Tipo**      | **Clave/Regla**    | **Nulo** | **Descripción**                  |
|-----------------|---------------|--------------------|----------|----------------------------------|
| id              | uuid          | PK                 | Sí       | Identificador.                   |
| tenant_id       | uuid          | FK tenants.id      | Sí       | Tenant.                          |
| nodo_plan_id    | uuid          | FK nodos_plan.id   | Sí       | Producto/programa asociado.      |
| indicador_id    | uuid          | FK indicadores.id  | Sí       | Indicador.                       |
| dependencia_id  | uuid          | FK dependencias.id | Sí       | Responsable líder.               |
| codigo          | varchar(80)   |                    | Sí       | Código.                          |
| descripcion     | text          |                    | Sí       | Meta.                            |
| linea_base      | numeric(18,4) |                    | No       | Valor inicial.                   |
| meta_cuatrienio | numeric(18,4) |                    | Sí       | Valor objetivo total.            |
| unidad_medida   | varchar(60)   |                    | Sí       | Unidad compatible con indicador. |
| ponderacion     | numeric(7,4)  |                    | No       | Peso en agregaciones.            |
| estado          | varchar(20)   |                    | Sí       | ACTIVA/SUSPENDIDA/CERRADA.       |

**Restricciones principales:** unique(tenant_id,codigo). \| ponderacion entre 0 y 100 si se usa como porcentaje.

**Índices sugeridos:** index(nodo_plan_id), index(dependencia_id), index(indicador_id)

## 7.12 programacion_anual_metas

Plan Indicativo anual por meta.

| **Campo**              | **Tipo**      | **Clave/Regla** | **Nulo** | **Descripción**        |
|------------------------|---------------|-----------------|----------|------------------------|
| id                     | uuid          | PK              | Sí       | Identificador.         |
| tenant_id              | uuid          | FK tenants.id   | Sí       | Tenant.                |
| meta_id                | uuid          | FK metas.id     | Sí       | Meta.                  |
| vigencia               | smallint      |                 | Sí       | Año.                   |
| valor_programado       | numeric(18,4) |                 | Sí       | Meta de la vigencia.   |
| presupuesto_programado | numeric(18,2) |                 | No       | Referencia financiera. |
| observacion            | text          |                 | No       | Justificación.         |

**Restricciones principales:** unique(meta_id,vigencia). \| vigencia dentro del rango del plan.

**Índices sugeridos:** index(tenant_id,vigencia), index(meta_id,vigencia)

## 7.13 avances_metas

Seguimiento físico periódico de metas.

| **Campo**         | **Tipo**      | **Clave/Regla** | **Nulo** | **Descripción**                |
|-------------------|---------------|-----------------|----------|--------------------------------|
| id                | uuid          | PK              | Sí       | Identificador.                 |
| tenant_id         | uuid          | FK tenants.id   | Sí       | Tenant.                        |
| meta_id           | uuid          | FK metas.id     | Sí       | Meta.                          |
| vigencia          | smallint      |                 | Sí       | Año.                           |
| periodo_tipo      | varchar(20)   |                 | Sí       | MES/TRIMESTRE/SEMESTRE/CORTE.  |
| periodo_numero    | smallint      |                 | Sí       | Número del periodo.            |
| fecha_corte       | date          |                 | Sí       | Fecha oficial.                 |
| valor_periodo     | numeric(18,4) |                 | Sí       | Ejecución del periodo.         |
| valor_acumulado   | numeric(18,4) |                 | Sí       | Acumulado.                     |
| porcentaje_avance | numeric(7,4)  |                 | No       | Derivado o congelado en corte. |
| estado_revision   | varchar(20)   |                 | Sí       | BORRADOR/VALIDADO/APROBADO.    |
| observacion       | text          |                 | No       | Análisis.                      |

**Restricciones principales:** unique(meta_id,fecha_corte). \| No permitir aprobar sin responsable/evidencia según política.

**Índices sugeridos:** index(meta_id,fecha_corte), index(tenant_id,vigencia,estado_revision)

## 7.14 planes_accion

Cabecera de Plan de Acción por dependencia/vigencia.

| **Campo**      | **Tipo**     | **Clave/Regla**    | **Nulo** | **Descripción**            |
|----------------|--------------|--------------------|----------|----------------------------|
| id             | uuid         | PK                 | Sí       | Identificador.             |
| tenant_id      | uuid         | FK tenants.id      | Sí       | Tenant.                    |
| dependencia_id | uuid         | FK dependencias.id | Sí       | Dependencia.               |
| vigencia       | smallint     |                    | Sí       | Año.                       |
| nombre         | varchar(200) |                    | Sí       | Nombre.                    |
| version        | integer      |                    | Sí       | Versión.                   |
| estado         | varchar(20)  |                    | Sí       | BORRADOR/APROBADO/CERRADO. |

**Restricciones principales:** unique(dependencia_id,vigencia,version).

**Índices sugeridos:** index(tenant_id,vigencia), index(dependencia_id,estado)

## 7.15 actividades_plan_accion

Actividades operativas vinculadas a una meta.

| **Campo**              | **Tipo**      | **Clave/Regla**     | **Nulo** | **Descripción**                                    |
|------------------------|---------------|---------------------|----------|----------------------------------------------------|
| id                     | uuid          | PK                  | Sí       | Identificador.                                     |
| tenant_id              | uuid          | FK tenants.id       | Sí       | Tenant.                                            |
| plan_accion_id         | uuid          | FK planes_accion.id | Sí       | Plan.                                              |
| meta_id                | uuid          | FK metas.id         | Sí       | Meta que soporta.                                  |
| responsable_usuario_id | uuid          | FK usuarios.id      | Sí       | Responsable.                                       |
| descripcion            | text          |                     | Sí       | Actividad.                                         |
| fecha_inicio           | date          |                     | Sí       | Inicio.                                            |
| fecha_fin              | date          |                     | Sí       | Fin.                                               |
| presupuesto_estimado   | numeric(18,2) |                     | No       | Estimado.                                          |
| porcentaje_avance      | numeric(7,4)  |                     | Sí       | Avance.                                            |
| estado                 | varchar(20)   |                     | Sí       | PENDIENTE/EN_EJECUCION/CUMPLIDA/VENCIDA/CANCELADA. |

**Restricciones principales:** fecha_fin \>= fecha_inicio. \| porcentaje_avance entre 0 y 100.

**Índices sugeridos:** index(plan_accion_id), index(meta_id), index(responsable_usuario_id,estado)

## 7.16 proyectos_inversion

Proyectos que materializan metas del PDT.

| **Campo**       | **Tipo**     | **Clave/Regla**    | **Nulo** | **Descripción**                                  |
|-----------------|--------------|--------------------|----------|--------------------------------------------------|
| id              | uuid         | PK                 | Sí       | Identificador.                                   |
| tenant_id       | uuid         | FK tenants.id      | Sí       | Tenant.                                          |
| codigo_interno  | varchar(80)  |                    | Sí       | Código.                                          |
| codigo_bpin     | varchar(50)  |                    | No       | BPIN cuando aplique.                             |
| nombre          | varchar(300) |                    | Sí       | Nombre.                                          |
| objetivo        | text         |                    | No       | Objetivo.                                        |
| dependencia_id  | uuid         | FK dependencias.id | Sí       | Responsable.                                     |
| vigencia_inicio | smallint     |                    | Sí       | Inicio.                                          |
| vigencia_fin    | smallint     |                    | Sí       | Fin.                                             |
| estado          | varchar(25)  |                    | Sí       | FORMULACION/VIABLE/EJECUCION/CERRADO/SUSPENDIDO. |
| fuente_origen   | varchar(40)  |                    | No       | MANUAL/PIIP/IMPORTACION/etc.                     |

**Restricciones principales:** unique(tenant_id,codigo_interno). \| vigencia_fin \>= vigencia_inicio.

**Índices sugeridos:** index(tenant_id,estado), index(dependencia_id), index(codigo_bpin)

## 7.17 proyecto_meta

Relación N:M proyectos-metas.

| **Campo**   | **Tipo**     | **Clave/Regla**           | **Nulo** | **Descripción**                        |
|-------------|--------------|---------------------------|----------|----------------------------------------|
| proyecto_id | uuid         | FK proyectos_inversion.id | Sí       | Proyecto.                              |
| meta_id     | uuid         | FK metas.id               | Sí       | Meta.                                  |
| peso_aporte | numeric(7,4) |                           | No       | Peso estimado del proyecto en la meta. |
| observacion | text         |                           | No       | Notas.                                 |

**Restricciones principales:** PK compuesta(proyecto_id,meta_id). \| peso_aporte 0..100.

**Índices sugeridos:** index(meta_id)

## 7.18 presupuestos_proyecto

Presupuesto de proyecto por vigencia y fuente.

| **Campo**              | **Tipo**      | **Clave/Regla**           | **Nulo** | **Descripción**         |
|------------------------|---------------|---------------------------|----------|-------------------------|
| id                     | uuid          | PK                        | Sí       | Identificador.          |
| tenant_id              | uuid          | FK tenants.id             | Sí       | Tenant.                 |
| proyecto_id            | uuid          | FK proyectos_inversion.id | Sí       | Proyecto.               |
| vigencia               | smallint      |                           | Sí       | Año.                    |
| fuente                 | varchar(120)  |                           | Sí       | Fuente de financiación. |
| apropiacion_inicial    | numeric(18,2) |                           | Sí       | Inicial.                |
| adiciones              | numeric(18,2) |                           | Sí       | Adiciones.              |
| reducciones            | numeric(18,2) |                           | Sí       | Reducciones.            |
| apropiacion_definitiva | numeric(18,2) |                           | Sí       | Resultado.              |
| origen_dato            | varchar(40)   |                           | Sí       | MANUAL/IMPORTADO/API.   |

**Restricciones principales:** Apropiación definitiva = inicial + adiciones - reducciones (salvo ajustes formalizados).

**Índices sugeridos:** index(proyecto_id,vigencia), index(tenant_id,vigencia)

## 7.19 ejecuciones_presupuestales

Cortes de ejecución financiera.

| **Campo**            | **Tipo**      | **Clave/Regla**             | **Nulo** | **Descripción**               |
|----------------------|---------------|-----------------------------|----------|-------------------------------|
| id                   | uuid          | PK                          | Sí       | Identificador.                |
| tenant_id            | uuid          | FK tenants.id               | Sí       | Tenant.                       |
| presupuesto_id       | uuid          | FK presupuestos_proyecto.id | Sí       | Presupuesto.                  |
| fecha_corte          | date          |                             | Sí       | Corte.                        |
| cdp                  | numeric(18,2) |                             | No       | CDP acumulado.                |
| rp_compromisos       | numeric(18,2) |                             | Sí       | Compromisos/RP.               |
| obligaciones         | numeric(18,2) |                             | Sí       | Obligaciones.                 |
| pagos                | numeric(18,2) |                             | Sí       | Pagos.                        |
| porcentaje_ejecucion | numeric(7,4)  |                             | No       | Derivado según regla elegida. |
| origen_dato          | varchar(40)   |                             | Sí       | MANUAL/IMPORTADO/API.         |

**Restricciones principales:** unique(presupuesto_id,fecha_corte). \| pagos \<= obligaciones \<= compromisos, salvo excepciones documentadas.

**Índices sugeridos:** index(presupuesto_id,fecha_corte), index(tenant_id,fecha_corte)

## 7.20 contratos_seguimiento

Seguimiento interno de contratos asociados a proyectos.

| **Campo**             | **Tipo**      | **Clave/Regla**           | **Nulo** | **Descripción**                                    |
|-----------------------|---------------|---------------------------|----------|----------------------------------------------------|
| id                    | uuid          | PK                        | Sí       | Identificador.                                     |
| tenant_id             | uuid          | FK tenants.id             | Sí       | Tenant.                                            |
| proyecto_id           | uuid          | FK proyectos_inversion.id | Sí       | Proyecto principal.                                |
| numero                | varchar(100)  |                           | Sí       | Número contractual.                                |
| secop_id              | varchar(150)  |                           | No       | Identificador externo. No asumir API.              |
| objeto                | text          |                           | Sí       | Objeto.                                            |
| contratista           | varchar(250)  |                           | Sí       | Nombre/razón social.                               |
| supervisor_usuario_id | uuid          | FK usuarios.id            | No       | Supervisor interno.                                |
| fecha_inicio          | date          |                           | No       | Inicio.                                            |
| fecha_fin             | date          |                           | No       | Fin.                                               |
| valor_inicial         | numeric(18,2) |                           | Sí       | Valor inicial.                                     |
| valor_actual          | numeric(18,2) |                           | Sí       | Valor tras modificaciones.                         |
| avance_fisico         | numeric(7,4)  |                           | No       | Último avance.                                     |
| avance_financiero     | numeric(7,4)  |                           | No       | Último avance.                                     |
| estado                | varchar(25)   |                           | Sí       | PLANEADO/EJECUCION/SUSPENDIDO/TERMINADO/LIQUIDADO. |

**Restricciones principales:** unique(tenant_id,numero). \| Porcentajes 0..100.

**Índices sugeridos:** index(proyecto_id), index(supervisor_usuario_id,estado), index(secop_id)

## 7.21 contrato_meta

Relación N:M contrato-meta.

| **Campo**       | **Tipo**     | **Clave/Regla**             | **Nulo** | **Descripción**  |
|-----------------|--------------|-----------------------------|----------|------------------|
| contrato_id     | uuid         | FK contratos_seguimiento.id | Sí       | Contrato.        |
| meta_id         | uuid         | FK metas.id                 | Sí       | Meta.            |
| aporte_estimado | numeric(7,4) |                             | No       | Aporte relativo. |
| observacion     | text         |                             | No       | Justificación.   |

**Restricciones principales:** PK compuesta(contrato_id,meta_id).

**Índices sugeridos:** index(meta_id)

## 7.22 evidencias

Metadatos de soportes asociados a cualquier entidad de negocio.

| **Campo**      | **Tipo**     | **Clave/Regla** | **Nulo** | **Descripción**                              |
|----------------|--------------|-----------------|----------|----------------------------------------------|
| id             | uuid         | PK              | Sí       | Identificador.                               |
| tenant_id      | uuid         | FK tenants.id   | Sí       | Tenant.                                      |
| entidad_tipo   | varchar(50)  |                 | Sí       | META/AVANCE/ACTIVIDAD/PROYECTO/CONTRATO/etc. |
| entidad_id     | uuid         |                 | Sí       | ID lógico de entidad.                        |
| nombre_archivo | varchar(255) |                 | Sí       | Nombre original.                             |
| storage_uri    | varchar(700) |                 | Sí       | Ruta privada.                                |
| mime_type      | varchar(120) |                 | Sí       | Tipo MIME.                                   |
| tamano_bytes   | bigint       |                 | Sí       | Tamaño.                                      |
| sha256         | varchar(64)  |                 | Sí       | Hash de integridad.                          |
| clasificacion  | varchar(30)  |                 | Sí       | PUBLICA/CLASIFICADA/RESERVADA/INTERNA.       |
| version        | integer      |                 | Sí       | Versión documental.                          |

**Restricciones principales:** Validar entidad_tipo contra catálogo. \| No exponer storage_uri directamente al cliente.

**Índices sugeridos:** index(tenant_id,entidad_tipo,entidad_id), index(sha256)

## 7.23 alertas_gestion

Alertas derivadas de reglas gerenciales.

| **Campo**        | **Tipo**    | **Clave/Regla** | **Nulo** | **Descripción**                                 |
|------------------|-------------|-----------------|----------|-------------------------------------------------|
| id               | uuid        | PK              | Sí       | Identificador.                                  |
| tenant_id        | uuid        | FK tenants.id   | Sí       | Tenant.                                         |
| tipo             | varchar(60) |                 | Sí       | DESVIACION_FISICO_FINANCIERA/META_ATRASADA/etc. |
| severidad        | varchar(15) |                 | Sí       | INFO/BAJA/MEDIA/ALTA/CRITICA.                   |
| entidad_tipo     | varchar(50) |                 | Sí       | Entidad afectada.                               |
| entidad_id       | uuid        |                 | Sí       | ID afectado.                                    |
| mensaje          | text        |                 | Sí       | Descripción.                                    |
| fecha_generacion | timestamptz |                 | Sí       | Generación.                                     |
| estado           | varchar(20) |                 | Sí       | ABIERTA/ATENDIDA/CERRADA.                       |
| regla_version    | varchar(30) |                 | No       | Versión de regla.                               |

**Restricciones principales:** Una alerta automática debe registrar regla y datos fuente.

**Índices sugeridos:** index(tenant_id,estado,severidad), index(entidad_tipo,entidad_id)

## 7.24 snapshots_reporte

Fotografías históricas de cortes e informes oficiales.

| **Campo**    | **Tipo**    | **Clave/Regla** | **Nulo** | **Descripción**                          |
|--------------|-------------|-----------------|----------|------------------------------------------|
| id           | uuid        | PK              | Sí       | Identificador.                           |
| tenant_id    | uuid        | FK tenants.id   | Sí       | Tenant.                                  |
| tipo         | varchar(40) |                 | Sí       | INFORME_GESTION/CORTE_PDT/DASHBOARD/etc. |
| periodo      | varchar(40) |                 | Sí       | Ej. 2026-T2.                             |
| fecha_corte  | timestamptz |                 | Sí       | Corte.                                   |
| payload      | jsonb       |                 | Sí       | Datos congelados.                        |
| payload_hash | varchar(64) |                 | Sí       | Hash.                                    |
| estado       | varchar(20) |                 | Sí       | BORRADOR/APROBADO/PUBLICADO.             |
| aprobado_by  | uuid        | FK usuarios.id  | No       | Aprobador.                               |
| aprobado_at  | timestamptz |                 | No       | Fecha.                                   |

**Restricciones principales:** Una versión APROBADA no se modifica.

**Índices sugeridos:** index(tenant_id,tipo,periodo), index(payload_hash)

## 7.25 audit_events

Bitácora inmutable de operaciones críticas.

| **Campo**      | **Tipo**    | **Clave/Regla** | **Nulo** | **Descripción**                          |
|----------------|-------------|-----------------|----------|------------------------------------------|
| id             | uuid        | PK              | Sí       | Identificador.                           |
| tenant_id      | uuid        | FK tenants.id   | Sí       | Tenant.                                  |
| usuario_id     | uuid        | FK usuarios.id  | No       | Actor; nulo para sistema.                |
| accion         | varchar(50) |                 | Sí       | CREATE/UPDATE/DELETE/APPROVE/EXPORT/etc. |
| entidad        | varchar(80) |                 | Sí       | Tabla/recurso.                           |
| entidad_id     | uuid        |                 | No       | Registro.                                |
| timestamp      | timestamptz |                 | Sí       | Momento.                                 |
| ip             | inet        |                 | No       | IP.                                      |
| correlation_id | uuid        |                 | No       | Operación transversal.                   |
| before_data    | jsonb       |                 | No       | Estado previo.                           |
| after_data     | jsonb       |                 | No       | Estado posterior.                        |
| metadata       | jsonb       |                 | No       | Contexto adicional.                      |

**Restricciones principales:** No UPDATE/DELETE desde aplicación ordinaria. \| Retención según política institucional.

**Índices sugeridos:** index(tenant_id,timestamp desc), index(entidad,entidad_id), index(correlation_id)

# 8. Reglas de integridad y negocio

- Una FK entre tablas de negocio no puede cruzar tenants. Validar en backend y, cuando sea posible, mediante claves compuestas o políticas RLS.

- Una meta debe pertenecer a un nodo del mismo Plan de Desarrollo y a una dependencia del mismo tenant.

- La programación anual de una meta debe ubicarse dentro de las vigencias del Plan de Desarrollo.

- Un avance aprobado no se elimina; las correcciones se realizan mediante nueva versión, reversión controlada o ajuste con trazabilidad.

- Proyecto-meta y contrato-meta deben permitir N:M; no agregar meta_id único en proyecto o contrato como única relación si puede existir aporte múltiple.

- El porcentaje físico y financiero debe ser calculable desde datos fuente; si se congela para un corte, conservar fórmula/versión.

- Las evidencias deben conservar hash de integridad y control de acceso.

- Los estados de aprobación deben respetar segregación de funciones cuando la política lo exija.

- Los reportes oficiales aprobados deben usar snapshot y no consultas en vivo para preservar el histórico.

- No usar borrado en cascada sobre información histórica aprobada o auditada.

# 9. Multitenancy y seguridad de datos

La V1 debe diseñarse como multi-tenant aun si el piloto inicia con una sola Alcaldía. El aislamiento es un requisito estructural y no una mejora posterior.

| **Control**    | **Implementación recomendada**                                                                 |
|----------------|------------------------------------------------------------------------------------------------|
| Tenant context | Resolver tenant en autenticación y propagarlo a cada request.                                  |
| Backend        | Toda consulta de negocio filtra por tenant_id de sesión.                                       |
| PostgreSQL     | Aplicar Row Level Security en tablas sensibles cuando la estrategia sea compatible con el ORM. |
| FK lógicas     | Validar que entidades relacionadas compartan tenant.                                           |
| Archivos       | Prefijo/bucket o namespace por tenant; URLs firmadas temporales.                               |
| Auditoría      | tenant_id obligatorio y correlation_id para operaciones complejas.                             |
| Pruebas        | Test automático de acceso cruzado Municipio A -\> registro Municipio B.                        |

# 10. Auditoría y trazabilidad

La auditoría debe ser transversal y separarse de los logs técnicos. Los eventos de auditoría representan acciones de negocio y deben ser consultables por control interno/auditoría según permisos.

- Creación o modificación de Plan de Desarrollo, estructura, metas e indicadores.

- Carga, validación y aprobación de avances.

- Cambios de presupuesto importado o manual.

- Asociación/desasociación de proyectos y contratos con metas.

- Aprobación/cierre de planes de acción e informes.

- Exportación de información sensible o reportes oficiales.

- Cambios de roles, permisos o estructura institucional.

# 11. Índices y rendimiento

- Indexar tenant_id como primera columna en consultas frecuentes multi-tenant.

- Índices compuestos recomendados: (tenant_id, vigencia), (tenant_id, estado), (meta_id, fecha_corte), (proyecto_id, vigencia).

- Usar índices parciales para estados activos/abiertos cuando el volumen lo justifique.

- Considerar materialized views para dashboards agregados solo después de medir consultas reales.

- Evitar recalcular árboles completos en cada request; usar CTE recursivos con índices o paths materializados si el volumen crece.

- Particionar audit_events por fecha cuando el volumen lo justifique.

# 12. Estrategia de versionamiento y snapshots

El modelo distingue datos operativos vivos de estados oficiales congelados. Planes, metas y avances pueden evolucionar; un corte aprobado debe conservar exactamente los valores usados en su momento.

| **Objeto**                | **Estrategia**                                                                                                |
|---------------------------|---------------------------------------------------------------------------------------------------------------|
| Plan de Desarrollo        | Campo version + estado; cambios estructurales relevantes generan nueva versión o acto modificatorio trazable. |
| Plan de Acción            | Versionado por dependencia y vigencia.                                                                        |
| Avances                   | Registros por corte; aprobación bloquea edición directa.                                                      |
| Informe/Dashboard oficial | snapshot_reporte con payload hash y aprobación.                                                               |
| Evidencias                | Versionadas y con hash SHA-256.                                                                               |
| Auditoría                 | Append-only.                                                                                                  |

# 13. Orden de implementación

16. Crear schemas y extensiones: pgcrypto, citext si se usan.

17. Crear tenants, municipios, administraciones y dependencias.

18. Crear usuarios, roles y asignaciones RBAC.

19. Crear Plan de Desarrollo y nodos jerárquicos.

20. Crear indicadores, metas y programación anual.

21. Crear avances de metas y flujo de revisión.

22. Crear Planes de Acción y actividades.

23. Crear proyectos y relación proyecto-meta.

24. Crear presupuesto y ejecuciones financieras.

25. Crear contratos y relación contrato-meta.

26. Crear evidencias, alertas y snapshots.

27. Crear audit_events y políticas de seguridad/RLS.

28. Agregar índices y pruebas de integridad.

29. Construir vistas/API agregadas para Dashboard del Alcalde.

# 14. Criterios de aceptación del modelo

- Se puede crear una Alcaldía/tenant y aislar completamente sus datos.

- Se puede representar un PDT con jerarquía configurable sin agregar nuevas tablas por cada nivel.

- Se puede programar cada meta por vigencia y registrar avances por corte.

- Se puede saber qué dependencia y qué usuario son responsables de cada actividad.

- Una meta puede estar asociada a varios proyectos y contratos.

- Se puede consultar desde una meta hasta su presupuesto, ejecución financiera, contratos y evidencias.

- Se puede calcular y explicar una desviación físico-financiera.

- Se puede congelar un corte oficial mediante snapshot.

- Toda operación crítica queda registrada en audit_events.

- Una prueba de seguridad demuestra que un usuario de un tenant no puede leer o modificar datos de otro.

# 15. Decisiones arquitectónicas abiertas

| **Decisión**           | **Recomendación V1**                                                                                                                |
|------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| ORM                    | SQLAlchemy 2 + Alembic si backend FastAPI.                                                                                          |
| RLS                    | Usarla en tablas críticas si las pruebas demuestran compatibilidad operativa; mantener filtro de tenant en backend de todas formas. |
| Jerarquía PDT          | Adjacency list (parent_id) en V1; evaluar ltree/materialized path si crece complejidad.                                             |
| Motor de indicadores   | Fórmulas parametrizadas seguras; nunca eval() de texto libre.                                                                       |
| Almacenamiento         | Objeto privado S3-compatible + metadatos en PostgreSQL.                                                                             |
| Integración financiera | Importación/API mediante adaptadores, no acoplar núcleo a un proveedor.                                                             |
| SECOP/SisPT/PIIP       | Diseñar interfaces de integración; validar API/capacidad oficial antes de implementar conectores.                                   |
| Auditoría              | Schema/base separada si el despliegue lo permite; eventos append-only.                                                              |

# Anexo A. Cadena de trazabilidad principal

La consulta estratégica que debe soportar la V1 es:

**PLAN DE DESARROLLO -\> NODO -\> META -\> INDICADOR -\> PROGRAMACIÓN -\> AVANCE -\> PROYECTO -\> PRESUPUESTO -\> EJECUCIÓN -\> CONTRATO -\> EVIDENCIA -\> ALERTA -\> SNAPSHOT -\> AUDITORÍA**

# Anexo B. Resultado técnico esperado

A partir de este documento, el siguiente artefacto técnico debe ser el paquete de migraciones iniciales de PostgreSQL/Alembic y los modelos ORM del Núcleo Central V1. La implementación debe respetar los nombres y relaciones aquí definidos o documentar formalmente cualquier desviación antes de programarla.
