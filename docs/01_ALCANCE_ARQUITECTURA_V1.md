**DOCUMENTO MAESTRO DE ALCANCE  
Y ARQUITECTURA V1**

**SIGM COLOMBIA**

Sistema Integral de Gestión Municipal

| **Documento** | Documento Maestro de Alcance y Arquitectura V1    |
|---------------|---------------------------------------------------|
| **Producto**  | SIGM Colombia                                     |
| **Versión**   | 1.0                                               |
| **Fecha**     | 6 de septiembre de 2026                           |
| **Estado**    | Base para diseño detallado y construcción del MVP |

Principio rector: el Plan de Desarrollo Municipal será el eje estratégico; los datos de ejecución, presupuesto, proyectos, contratos, evidencias, riesgos y resultados deberán poder trazarse hasta las metas del Plan.

# 1. Resumen ejecutivo

Este documento define el alcance funcional, la arquitectura y la hoja de ruta de la versión 1 (V1) de SIGM Colombia, una plataforma modular de gestión pública orientada a alcaldías colombianas. Su propósito es conectar planeación territorial, ejecución y control mediante una fuente única de información y trazabilidad.

La V1 no busca reemplazar de inmediato los sistemas contables, de nómina, tesorería, SECOP o plataformas oficiales del Estado. Se concentra en construir el “cerebro gerencial” de la administración municipal: Plan de Desarrollo, Plan Indicativo, metas, indicadores, Planes de Acción, proyectos, seguimiento físico-financiero, evidencias, alertas, reportes y Dashboard del Alcalde.

La arquitectura se diseña desde el origen para múltiples alcaldías (multitenancy), control de acceso por roles, segregación de funciones, auditoría, versionamiento, seguridad, trazabilidad legal e interoperabilidad futura.

## 1.1 Propuesta de valor

- Convertir el Plan de Desarrollo Municipal en el núcleo operativo y medible de la gestión.

- Permitir saber no solo cuánto dinero se ejecutó, sino qué meta, proyecto y resultado se produjo con ese recurso.

- Detectar desviaciones entre ejecución física y financiera antes de que se conviertan en incumplimientos.

- Generar información consolidada para decisiones de alcalde, secretarías, planeación, control interno y ciudadanía.

- Reducir duplicidad de datos, hojas de cálculo aisladas y reprocesos en informes de gestión.

# 2. Alcance de la V1 (MVP estratégico)

La V1 incluye los componentes estrictamente necesarios para demostrar el valor central de SIGM y validar el producto en una alcaldía piloto.

| **Componente V1**            | **Alcance**                                                                                              |
|------------------------------|----------------------------------------------------------------------------------------------------------|
| Núcleo institucional         | Municipio, administración, periodo de gobierno, dependencias, usuarios, roles, permisos y configuración. |
| Plan de Desarrollo Municipal | Estructura parametrizable de líneas, sectores, programas, productos, metas e indicadores.                |
| Plan Indicativo              | Programación anual/cuatrienal de metas y seguimiento acumulado.                                          |
| Planes de Acción             | Actividades y compromisos de las dependencias vinculados con metas del Plan.                             |
| Indicadores                  | Fichas técnicas, metas, resultados, periodicidad, responsable, fuente y evidencia.                       |
| Proyectos de inversión       | Registro y relación con metas, productos, presupuesto, localización y población beneficiaria.            |
| Seguimiento físico           | Programado, ejecutado, acumulado, porcentaje, estado, observaciones y evidencia.                         |
| Seguimiento financiero       | Apropiación, compromisos, obligaciones, pagos o valores importados desde el sistema financiero.          |
| Cruce físico-financiero      | Comparación automática y alertas de desviación.                                                          |
| Evidencias                   | Repositorio de soportes vinculados con metas, proyectos, actividades e indicadores.                      |
| Dashboard del Alcalde        | Vista ejecutiva del avance PDT, metas críticas, ejecución, proyectos y alertas.                          |
| Reportes                     | Informe de seguimiento, informe por secretaría, metas, indicadores y resumen ejecutivo.                  |
| Auditoría y versionamiento   | Registro de cambios, estados de aprobación y conservación histórica.                                     |

## 2.1 Fuera de alcance en V1

- Contabilidad general

- Tesorería transaccional

- Nómina

- Gestión completa SECOP

- SGDEA completo

- PQRSD completo

- Talento humano completo

- SG-SST completo

- Gestión jurídica completa

- Inventario y activos completo

- Portal ciudadano avanzado

Estos componentes se diseñarán como integraciones o fases posteriores. La V1 dejará contratos de interfaz y puntos de extensión para incorporarlos sin rediseñar el núcleo.

# 3. Posicionamiento competitivo después del análisis de mercado

SIGM no se posicionará inicialmente como un ERP contable ni como un software MIPG aislado. Su diferenciador será la integración de la gestión municipal alrededor del Plan de Desarrollo.

**SisPT - DNP:** Referente oficial para PDT y seguimiento territorial. SIGM debe interoperar y no intentar sustituirlo.

**IDEAL.10:** Competidor comercial más cercano a un ERP territorial. SIGM debe diferenciarse en trazabilidad gerencial y resultados.

**Pensemos:** Referente fuerte en gestión estratégica, indicadores, riesgos y MIPG.

**Daruma:** Referente fuerte en sistemas de gestión, auditoría, riesgos y mejora.

Mensaje de posicionamiento recomendado: “SIGM no solo muestra cuánto ha gastado la Alcaldía; muestra qué resultado del Plan de Desarrollo produjo ese gasto.”

# 4. Núcleo central de SIGM

El núcleo central será estable y compartido por todos los módulos actuales y futuros.

Entidad territorial → Administración / periodo → Dependencia → **Plan de Desarrollo** → Línea / sector / programa → Producto → **Meta** → Indicador → Plan de Acción → **Proyecto** → Presupuesto / fuente → Contrato (referenciado) → **Avance físico** → **Avance financiero** → Evidencia → Riesgo / alerta → **Resultado** → Informe

# 5. Modelo de dominio V1

| **Entidad**         | **Responsabilidad**                                              |
|---------------------|------------------------------------------------------------------|
| Tenant / Entidad    | Aísla cada alcaldía y sus datos.                                 |
| Municipio           | Identificación territorial y configuración institucional.        |
| PeriodoGobierno     | Vincula administración, alcalde y vigencia constitucional.       |
| Dependencia         | Secretarías, oficinas, direcciones y responsables.               |
| PlanDesarrollo      | Cabecera del PDT y versiones.                                    |
| NivelPlan           | Estructura flexible: dimensión, línea, sector, programa u otros. |
| Producto            | Bien o servicio asociado al programa.                            |
| Meta                | Unidad principal de compromiso y seguimiento.                    |
| Indicador           | Ficha técnica y serie de resultados.                             |
| PlanIndicativo      | Programación anual/cuatrienal de la meta.                        |
| PlanAccion          | Compromisos de cada dependencia.                                 |
| Proyecto            | Proyecto de inversión relacionado con metas.                     |
| FuenteFinanciacion  | Origen de recursos.                                              |
| EjecucionFisica     | Avance periódico de meta/proyecto.                               |
| EjecucionFinanciera | Valores financieros reportados o importados.                     |
| Evidencia           | Archivos y referencias que soportan avances.                     |
| Alerta              | Desviaciones, vencimientos y riesgos.                            |
| Aprobacion          | Workflow de revisión/aprobación.                                 |
| Auditoria           | Histórico inmutable de eventos críticos.                         |

# 6. Arquitectura técnica V1

## 6.1 Vista lógica

**Frontend:** React/Next.js + TypeScript. Componentes reutilizables, accesibilidad y dashboards responsive.

**API:** FastAPI/Python. Contratos OpenAPI, validaciones, autenticación, reglas de negocio y servicios de reportes.

**Dominio:** Módulos separados por contextos: institucional, planeación, indicadores, proyectos, seguimiento, evidencias, reporting.

**Persistencia:** PostgreSQL. Integridad referencial, índices, versionamiento y RLS cuando aplique.

**Archivos:** S3/MinIO o almacenamiento privado equivalente; metadatos y hash en PostgreSQL.

**Auditoría:** Esquema o base separada sigm_audit para eventos críticos.

**Cache/colas:** Redis opcional para cache, notificaciones y trabajos asíncronos controlados.

**Observabilidad:** Logs estructurados, métricas, health checks y trazas cuando sea viable.

**Despliegue:** Contenedores, reverse proxy, TLS, entornos separados y copias de seguridad verificadas.

## 6.2 Arquitectura multitenant

- tenant_id obligatorio en entidades de negocio

- validación de tenant en backend

- RBAC y alcance por dependencia

- Row Level Security de PostgreSQL cuando sea apropiado

- pruebas automáticas de aislamiento entre alcaldías

- almacenamiento de archivos separado por tenant

- auditoría con tenant y correlación de operación

# 7. Actores, roles y segregación de funciones

| **Rol**                 | **Responsabilidad V1**                                                             |
|-------------------------|------------------------------------------------------------------------------------|
| Superadministrador      | Administración global sin acceso funcional indiscriminado a información municipal. |
| Administrador Alcaldía  | Configura la entidad, usuarios y parámetros.                                       |
| Alcalde                 | Consulta tablero, revisa y aprueba información gerencial definida.                 |
| Planeación              | Administra PDT, plan indicativo, metas, indicadores y seguimiento.                 |
| Hacienda                | Suministra/valida datos financieros e integraciones.                               |
| Secretario de Despacho  | Reporta y valida metas, proyectos y planes de acción de su dependencia.            |
| Control Interno         | Consulta, audita y verifica; no debe alterar datos fuente.                         |
| Responsable de Proyecto | Registra avances y evidencias del proyecto.                                        |
| Consulta                | Lectura según permisos.                                                            |

Regla de segregación: siempre que el proceso lo requiera, quien registra no debe ser quien aprueba. Los flujos deberán permitir REGISTRA → REVISA → APRUEBA.

# 8. Especificación funcional de módulos V1

## 8.1 Núcleo institucional

- Datos de entidad y municipio

- Periodo de gobierno

- Estructura organizacional

- Dependencias y responsables

- Parámetros generales

- Usuarios, roles y permisos

## 8.2 Plan de Desarrollo

- Versiones del plan

- Estructura jerárquica parametrizable

- Metas de resultado y producto

- Indicadores vinculados

- Responsables

- Documentos oficiales y actos de aprobación

## 8.3 Plan Indicativo

- Programación por vigencia

- Meta cuatrienal

- Acumulados

- Proyección de cumplimiento

- Modificaciones versionadas

## 8.4 Planes de Acción

- Dependencia

- Actividad

- Meta relacionada

- Responsable

- Fechas

- Presupuesto

- Estado

- Evidencia

## 8.5 Indicadores

- Ficha técnica

- Fórmula

- Unidad

- Línea base

- Meta

- Periodicidad

- Fuente

- Responsable

- Resultados históricos

## 8.6 Proyectos

- Código/BPIN cuando aplique

- Sector/programa/producto

- Metas relacionadas

- Beneficiarios

- Localización

- Presupuesto y fuentes

- Estado y avances

## 8.7 Seguimiento físico-financiero

- Corte periódico

- Programado vs ejecutado

- Ejecución financiera importada o registrada

- Desviación

- Justificación

- Evidencia

- Aprobación

## 8.8 Dashboard del Alcalde

- Avance global PDT

- Avance por secretaría

- Ejecución financiera

- Metas críticas

- Metas sin reporte

- Proyectos en riesgo

- Desviaciones físico-financieras

- Alertas

## 8.9 Evidencias

- Archivo/referencia

- Hash

- Tipo

- Fecha

- Origen

- Clasificación de acceso

- Versión

- Relación con meta/proyecto/avance

## 8.10 Reportes

- Seguimiento PDT

- Informe por dependencia

- Informe de metas

- Informe de indicadores

- Resumen gerencial

- Exportación PDF/Excel en fases de madurez de V1

## 8.11 Auditoría

- Usuario

- Acción

- Fecha/hora

- IP si aplica

- Entidad afectada

- Valor anterior/nuevo

- Tenant

- Correlación

# 9. Dashboard del Alcalde - indicadores prioritarios

- % avance global del Plan de Desarrollo

- % ejecución financiera consolidada

- metas cumplidas / totales

- metas críticas

- metas sin reporte

- metas con desviación físico-financiera

- avance por secretaría

- avance por sector

- proyectos activos

- proyectos atrasados

- presupuesto por fuente

- alertas críticas

- tendencia de cumplimiento cuatrienal

El dashboard debe permitir drill-down: Alcaldía → Secretaría → Programa → Meta → Proyecto → avance → evidencia.

# 10. Matriz legal inicial de V1

La matriz legal debe ser versionada, parametrizable y validada periódicamente. Esta tabla constituye el marco inicial para diseño; no reemplaza concepto jurídico ni revisión de vigencia específica para cada entidad.

| **Tema**                     | **Norma base**                                                   | **Requisito funcional interpretado**                                                                                                                            | **Impacto en SIGM**                                                     |
|------------------------------|------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------|
| Planeación territorial       | Ley 152 de 1994                                                  | Procedimientos y mecanismos de elaboración, aprobación, ejecución, seguimiento, evaluación y control de planes de desarrollo; aplica a entidades territoriales. | Plan de Desarrollo, Plan Indicativo, seguimiento.                       |
| MIPG                         | Decreto 1499 de 2017 / Decreto 1083 de 2015                      | MIPG como marco para dirigir, planear, ejecutar, hacer seguimiento, evaluar y controlar gestión pública orientada a resultados y planes de desarrollo.          | Arquitectura de gestión, indicadores, seguimiento y futuro módulo MIPG. |
| Control Interno              | Ley 87 de 1993                                                   | Sistema de control interno integrado con planeación, información, evaluación, indicadores e informes de gestión.                                                | Auditoría, trazabilidad, reportes, planes de mejora futuros.            |
| Rendición de cuentas         | Ley 1757 de 2015                                                 | Proceso de información, explicación, diálogo y evaluación de la gestión ante ciudadanía y control social.                                                       | Base de datos de resultados e insumos para futura rendición de cuentas. |
| Transparencia                | Ley 1712 de 2014                                                 | Acceso a información pública y principio de máxima publicidad, con excepciones legales.                                                                         | Clasificación, reportes y futura publicación de información.            |
| PTEP / anticorrupción        | Ley 2195 de 2022, art. 31                                        | Entidades municipales deben implementar Programas de Transparencia y Ética Pública y gestionar riesgos de corrupción.                                           | Modelo de riesgos y futura fase PTEP.                                   |
| Contratación estatal         | Ley 80 de 1993                                                   | Reglas y principios de contratos de entidades estatales; municipios son entidades estatales para sus efectos.                                                   | Referencia de contratos y trazabilidad proyecto-meta.                   |
| Contratación / transparencia | Ley 1150 de 2007                                                 | Medidas de eficiencia y transparencia y modalidades de selección.                                                                                               | Integración futura con seguimiento contractual.                         |
| Reglamentación contratación  | Decreto 1082 de 2015                                             | Reglamentación aplicable al sector de planeación y contratación estatal.                                                                                        | Diseño de integraciones y catálogos contractuales futuros.              |
| Presupuesto                  | Decreto 111 de 1996 + estatuto territorial aplicable             | Marco orgánico presupuestal; el diseño debe respetar normas territoriales y sistemas oficiales.                                                                 | Importación/relación de apropiación, compromiso, obligación y pago.     |
| Archivos                     | Ley 594 de 2000                                                  | Obliga organización, preservación y control de archivos públicos; permite nuevas tecnologías con autenticidad e integridad.                                     | Evidencias, metadatos, hash, retención, futura integración SGDEA.       |
| Datos personales             | Ley 1581 de 2012                                                 | Protección de datos personales en bases de datos públicas y privadas.                                                                                           | Privacidad, clasificación y controles de acceso.                        |
| Trámites                     | Ley 2052 de 2020                                                 | Racionalización, digitalización, automatización e interoperabilidad de trámites de entidades territoriales.                                                     | Criterios de interoperabilidad; módulo de trámites posterior.           |
| Empleo público               | Ley 909 de 2004                                                  | Regula empleo público, carrera administrativa y gerencia pública.                                                                                               | Roles institucionales y futura gestión de talento humano.               |
| SG-SST                       | Ley 1562 de 2012, Decreto 1072 de 2015 y Resolución 0312 de 2019 | Marco de Seguridad y Salud en el Trabajo aplicable a entidades empleadoras.                                                                                     | Fase posterior SG-SST; no se mezcla con núcleo PDT en V1.               |

## 10.1 Estructura obligatoria de trazabilidad normativa

| **Norma**          | **Artículo**       | **Requisito**      | **Proceso**        | **Módulo**         | **Funcionalidad**  | **Evidencia**      | **Responsable**    | **Estado**         |
|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|
| \[Parametrizable\] | \[Parametrizable\] | \[Parametrizable\] | \[Parametrizable\] | \[Parametrizable\] | \[Parametrizable\] | \[Parametrizable\] | \[Parametrizable\] | \[Parametrizable\] |

Regla: ninguna norma deberá quedar “quemada” como lógica rígida cuando pueda administrarse desde catálogo. Se debe conservar fuente oficial, estado de vigencia, fecha de validación, norma modificatoria/derogatoria y responsable jurídico.

# 11. Seguridad, privacidad y auditoría

- MFA para perfiles privilegiados cuando sea viable

- contraseñas robustas y sesiones seguras

- RBAC y permisos por tenant/dependencia

- validación backend; el frontend nunca será control suficiente

- protección contra IDOR

- cifrado TLS

- secretos fuera del repositorio

- registro de eventos de seguridad

- rate limiting para endpoints sensibles

- backups cifrados y pruebas de restauración

- clasificación de información pública, clasificada, reservada, personal y sensible

- logs sin exposición de secretos ni datos personales innecesarios

# 12. Estrategia de integraciones V1

SIGM debe interoperar con sistemas externos mediante una capa de adaptadores. No se deberán crear integraciones ficticias ni depender directamente de estructuras no documentadas.

| **Sistema externo**          | **Enfoque**                                                                                      | **Prioridad** |
|------------------------------|--------------------------------------------------------------------------------------------------|---------------|
| SisPT                        | Exportación/importación o conciliación de datos PDT cuando los mecanismos oficiales lo permitan. | Alta          |
| Sistema financiero municipal | Importar ejecución presupuestal y financiera para evitar doble digitación.                       | Alta          |
| SECOP                        | Referenciar procesos/contratos; integración solo con mecanismos oficiales disponibles.           | Media         |
| PIIP / BPIN                  | Relacionar proyectos cuando aplique y exista mecanismo permitido.                                | Media         |
| CUIPO / CHIP                 | Evaluar reportes e intercambio en fases posteriores.                                             | Media         |
| FURAG                        | Soporte de evidencia; no automatizar respuestas institucionales.                                 | Baja V1       |

# 13. Gobierno y calidad de datos

- Fuente única por entidad de negocio

- catálogos normalizados

- campos obligatorios y reglas de validación

- periodos de corte y bloqueo de versiones aprobadas

- responsable y fecha de cada dato

- evidencia asociada cuando corresponda

- snapshots de reportes aprobados

- no permitir sobrescritura silenciosa de históricos

- reglas de consistencia entre avance físico y financiero

# 14. Flujos de negocio prioritarios

**Carga inicial del PDT:** Planeación configura estructura → importa/crea metas → valida indicadores → aprueba versión.

**Programación anual:** Planeación distribuye meta cuatrienal → secretaría valida → se aprueba Plan Indicativo.

**Reporte periódico:** Responsable registra avance → adjunta evidencia → secretario revisa → Planeación valida → dato entra al consolidado.

**Desviación:** Motor compara físico y financiero → genera alerta → responsable justifica → se registra acción.

**Cierre de periodo:** Se bloquea corte aprobado → se crea snapshot → reportes consumen datos cerrados.

**Consulta gerencial:** Alcalde visualiza dashboard → drill-down hasta meta/proyecto/evidencia.

# 15. Fases de desarrollo

| **Fase** | **Resultado**                                                                                    |
|----------|--------------------------------------------------------------------------------------------------|
| Fase 0   | Descubrimiento y validación con una alcaldía piloto; inventario de procesos, fuentes y sistemas. |
| Fase 1   | Arquitectura, repositorio, estándares, CI/CD, seguridad base y multitenancy.                     |
| Fase 2   | Núcleo institucional, usuarios, roles, dependencias y periodos.                                  |
| Fase 3   | Plan de Desarrollo, jerarquía, metas, productos e indicadores.                                   |
| Fase 4   | Plan Indicativo y programación anual/cuatrienal.                                                 |
| Fase 5   | Planes de Acción.                                                                                |
| Fase 6   | Proyectos de inversión.                                                                          |
| Fase 7   | Seguimiento físico.                                                                              |
| Fase 8   | Importación/seguimiento financiero.                                                              |
| Fase 9   | Motor de desviación físico-financiera y alertas.                                                 |
| Fase 10  | Evidencias, versionamiento y snapshots.                                                          |
| Fase 11  | Dashboard del Alcalde y dashboards sectoriales.                                                  |
| Fase 12  | Reportes y exportaciones.                                                                        |
| Fase 13  | Auditoría, seguridad avanzada y pruebas de aislamiento.                                          |
| Fase 14  | Piloto real, correcciones y estabilización.                                                      |
| Fase 15  | Producción V1 y medición de adopción.                                                            |

# 16. Criterios de aceptación de V1

1.  Una alcaldía puede configurarse sin afectar datos de otra.

2.  Planeación puede registrar o importar un Plan de Desarrollo completo y versionado.

3.  Cada meta puede relacionarse con indicador, dependencia, programación anual, proyecto y evidencia.

4.  Cada dependencia puede reportar avances con workflow de validación.

5.  El sistema calcula avance físico y acumulado de manera reproducible.

6.  El sistema registra o importa datos financieros y calcula ejecución.

7.  El motor identifica desviaciones físico-financieras según umbrales configurables.

8.  El alcalde puede navegar desde el indicador general hasta la evidencia de una meta.

9.  Los reportes de un corte aprobado permanecen históricamente estables.

10. Existe auditoría de cambios críticos y pruebas de acceso cruzado entre tenants.

11. La matriz legal permite asociar requisito → módulo → evidencia.

12. Las APIs principales están documentadas y cubiertas por pruebas de integración.

# 17. Indicadores de éxito del piloto

- % de metas del PDT cargadas correctamente

- % de metas con responsable e indicador válido

- % de reportes periódicos presentados dentro del plazo

- reducción del tiempo de consolidación de informes

- número de hojas de cálculo reemplazadas

- % de metas con evidencia trazable

- tiempo para identificar una meta crítica

- uso mensual por secretarios y alcalde

- número de incidencias de calidad de datos

- cero accesos cruzados entre tenants

# 18. Riesgos del proyecto y mitigación

| **Riesgo**                                  | **Mitigación**                                              |
|---------------------------------------------|-------------------------------------------------------------|
| Alcance excesivo                            | Congelar V1; nuevos módulos pasan a backlog.                |
| Duplicación con sistemas existentes         | Integrar/importar en lugar de reemplazar.                   |
| Datos de baja calidad                       | Validaciones, responsables, cortes y evidencia.             |
| Resistencia institucional                   | Piloto con Planeación y una o dos secretarías; UX sencilla. |
| Cambios normativos                          | Matriz legal versionada y catálogos configurables.          |
| Dependencia de integraciones no disponibles | Adaptadores y mecanismos de importación manual controlada.  |
| Seguridad/multitenancy                      | Pruebas automatizadas, RLS y segregación.                   |
| Informes que cambian retroactivamente       | Snapshots y versionamiento de cierres.                      |

# 19. Entregables técnicos siguientes

13. Diagrama ER detallado de V1

14. Diccionario de datos

15. Especificación OpenAPI inicial

16. Matriz de roles y permisos por acción

17. Wireframes del Dashboard del Alcalde

18. Matriz legal detallada por artículo

19. Matriz de integraciones y formatos de intercambio

20. Backlog de historias de usuario y criterios de aceptación

21. Plan de pruebas

22. Plan de despliegue y seguridad

# 20. Decisión de inicio recomendada

Iniciar la construcción por el NÚCLEO INSTITUCIONAL + PLAN DE DESARROLLO + INDICADORES + PLAN INDICATIVO. No comenzar simultáneamente módulos administrativos secundarios.

Cuando estos cuatro componentes estén estables, se incorpora Plan de Acción, proyectos y seguimiento físico-financiero. Esta secuencia reduce riesgo de rehacer el modelo de datos y mantiene el producto alineado con su ventaja competitiva.

# 21. Referencias normativas y fuentes oficiales consultadas

- **Ley 152 de 1994 - Ley Orgánica del Plan de Desarrollo:** https://www.secretariasenado.gov.co/senado/basedoc/ley_0152_1994.html

- **Decreto 1499 de 2017 - MIPG:** https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?5=&i=83433

- **Ley 87 de 1993 - Control Interno:** https://www.secretariasenado.gov.co/senado/basedoc/ley_0087_1993.html

- **Ley 1757 de 2015 - Rendición de Cuentas:** https://www.secretariasenado.gov.co/senado/basedoc/ley_1757_2015_pr001.html

- **Ley 1712 de 2014 - Transparencia y acceso a información pública:** https://www.secretariasenado.gov.co/senado/basedoc/ley_1712_2014.html

- **Ley 2195 de 2022 - Transparencia y ética pública:** https://www.secretariasenado.gov.co/senado/basedoc/ley_2195_2022.html

- **Ley 80 de 1993 - Contratación estatal:** https://www.secretariasenado.gov.co/senado/basedoc/ley_0080_1993.html

- **Ley 1150 de 2007 - Eficiencia y transparencia contractual:** https://www.secretariasenado.gov.co/senado/basedoc/ley_1150_2007.html

- **Decreto 111 de 1996 - Estatuto Orgánico del Presupuesto:** https://www.secretariasenado.gov.co/senado/basedoc/decreto_0111_1996.html

- **Ley 594 de 2000 - Ley General de Archivos:** https://www.secretariasenado.gov.co/senado/basedoc/ley_0594_2000.html

- **Ley 1581 de 2012 - Protección de datos personales:** https://www.secretariasenado.gov.co/senado/basedoc/ley_1581_2012.html

- **Ley 2052 de 2020 - Racionalización y digitalización de trámites:** https://www.secretariasenado.gov.co/senado/basedoc/ley_2052_2020.html

- **Ley 909 de 2004 - Empleo público y gerencia pública:** https://www.secretariasenado.gov.co/senado/basedoc/ley_0909_2004.html

Nota jurídica: el sistema deberá mantener revisión periódica de vigencia, modificaciones, derogatorias y reglamentación aplicable. La matriz legal de producto es un mecanismo de trazabilidad de software y no sustituye la función jurídica de la entidad.
