import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.schemas.importacion import ImportacionCreate, ImportacionRead, ImportacionErrorRow
from app.services.importacion import ImportacionService

router = APIRouter(prefix="/importaciones", tags=["importaciones"])


@router.post("/previsualizar", response_model=dict)
async def previsualizar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: uuid.UUID = Depends(get_current_user),
):
    """Preview import file and return errors/approved rows."""
    file_data = await file.read()
    service = ImportacionService(db)
    result = service.previsualizar(file_data, file.filename, creator=current_user)
    return result


@router.get("/{importacion_id}", response_model=ImportacionRead)
def get_importacion(importacion_id: uuid.UUID, db: Session = Depends(get_db)):
    """Get importacion detail."""
    from app.repositories.importacion import ImportacionRepository
    repo = ImportacionRepository(db)
    importacion = repo._session.get(Importacion, importacion_id)
    if importacion is None:
        raise HTTPException(status_code=404, detail="Importación no encontrada")
    return importacion


@router.post("/{importacion_id}/confirmar", response_model=dict)
def confirmar_importacion(
    importacion_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: uuid.UUID = Depends(get_current_user),
):
    """Confirm and apply the import."""
    service = ImportacionService(db)
    result = service.confirm_import(importacion_id, current_user)
    return result