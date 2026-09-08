from __future__ import annotations

from typing import Optional

from sqlalchemy import select

from app.models.importacion import Importacion
from app.repositories.base import BaseRepository


class ImportacionRepository(BaseRepository[Importacion]):
    def __init__(self, db):
        super().__init__(Importacion)

    def get_by_tenant(self, tenant_id: uuid.UUID) -> list[Importacion]:
        stmt = select(Importacion).where(Importacion.tenant_id == tenant_id)
        return list(self._session.exec(stmt).all())

    def get_preview(self, importacion_id: uuid.UUID) -> Optional[dict]:
        stmt = select(Importacion).where(Importacion.id == importacion_id)
        importacion = self._session.exec(stmt).one_or_none()
        if importacion is None:
            return None
        return {
            "id": str(importacion.id),
            "tipo": importacion.tipo,
            "filename": importacion.filename,
            "sha256_archivo": importacion.sha256_archivo,
            "creator": str(importacion.creator) if importacion.creator else None,
            "created_at": importacion.created_at,
            "confirmed_at": importacion.confirmed_at,
            "payload_canonico": importacion.payload_canonico,
            "state": "confirmed" if importacion.confirmed_at else "pending",
        }

    def validate_rows(self, importacion_id: uuid.UUID) -> dict:
        importacion = self._session.get(Importacion, importacion_id)
        if importacion is None:
            return {"approved": 0, "rejected": 0, "errors": ["Importación no encontrada"]}
        
        errors = importacion.payload_canonico.get("errors", []) if importacion.payload_canonico else []
        approved = importacion.payload_canonico.get("rows_approved", 0) if importacion.payload_canonico else 0
        rejected = importacion.payload_canonico.get("rows_rejected", 0) if importacion.payload_canonico else 0
        
        return {
            "approved": approved,
            "rejected": rejected,
            "errors": errors,
            "state": "validated" if not errors else "with_errors",
        }

    def confirm_import(self, importacion_id: uuid.UUID, confirmed_by: uuid.UUID) -> Importacion:
        importacion = self._session.get(Importacion, importacion_id)
        if importacion is None:
            raise ValueError("Importación no encontrada")
        importacion.confirmed_at = datetime.now()
        importacion.creator = confirmed_by
        self._session.add(importacion)
        self._session.flush()
        return importacion