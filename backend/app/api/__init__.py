from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.fases import router as fases_router
from app.api.v1.planeacion import router as planeacion_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router)
api_router.include_router(planeacion_router)
api_router.include_router(fases_router)
