# Aprendizajes del Agente

Los aprendizajes más recientes deben agregarse arriba.

---

- **2026-09-06 — Fases 5-13 completadas:**
  **Contexto:** Implementación masiva de todos los módulos de ejecución, presupuesto, control y reportes.
  **Aprendizaje:** Cuando se crean endpoints FastAPI, los parámetros con default (query params) deben ir después de los Depends sin default. El orden importa para la sintaxis de Python.
  **Aplicación futura:** Siempre poner Depends(tenant_id), Depends(current_user), Depends(db) antes de query params opcionales.

- **2026-09-06 — SQLAlchemy 2 + DeclarativeBase:**
  **Contexto:** Modelos escritos para SA 1.x con `Mapped = mapped_column(...)` sin tipo genérico.
  **Aprendizaje:** SA 2 con DeclarativeBase requiere `Mapped[type]` explícito o `__allow_unmapped__ = True` en la clase Base. El campo `metadata` es reservado por SQLAlchemy.
  **Aplicación futura:** Usar siempre `Mapped[uuid.UUID]` en lugar de `Mapped` bare. Renombrar campos que colisionen con atributos de SQLAlchemy.

- **2026-09-06 — FastAPI dependency injection order:**
  **Contexto:** CurrentUser y CurrentTenantId se declaraban antes de las funciones que referencian.
  **Aprendizaje:** Con Annotated[], las funciones deben existir antes de crear los tipos Annotated que las referencian.
  **Aplicación futura:** Declarar funciones de dependencia antes de crear los tipos Annotated.

- **2026-09-06 — Fase 3 completada:**
  **Contexto:** Implementación de Plan de Desarrollo y nodos jerárquicos.
  **Aprendizaje:** El patrón adjacency list (parent_id) funciona bien para jerarquías simples.
  **Aplicación futura:** Siempre validar que el nodo padre pertenezca al mismo plan antes de crear hijos.

- **2026-09-06 — Fase 2 completada:**
  **Contexto:** Implementación de seguridad y multitenancy.
  **Aprendizaje:** El filtro tenant_id en repositories garantiza aislamiento a nivel de aplicación.
  **Aplicación futura:** Siempre crear repository base antes de services específicos.

<!-- Nuevos aprendizajes debajo de esta línea -->
