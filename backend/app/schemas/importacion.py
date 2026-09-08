from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, validator


class ImportacionTipo(StrEnum):
    PDT = "PDT"
    INDICADOR = "INDICADOR"
    INDICADORES = "INDICADORES"
    META = "META"
    PRESUPUESTO = "PRESUPUESTO"
    EJECUCION = "EJECUCION"


class ImportacionCreate(BaseModel):
    tipo: ImportacionTipo
    filename: str = Field(min_length=1, max_length=255)
    sha256_archivo: str = Field(min_length=1, max_length=64)
    payload_canonico: dict[str, Any] | None = None
    creator: uuid.UUID | None = None


class ImportacionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    tipo: ImportacionTipo
    filename: str
    sha256_archivo: str
    payload_canonico: dict[str, Any] | None
    creator: uuid.UUID | None
    created_at: datetime
    confirmed_at: datetime | None


class ImportacionErrorRow(BaseModel):
    row: int | None
    field: str | None
    code: str
    message: str


class ImportacionConfirmation(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    tipo: ImportacionTipo
    filename: str
    sha256_archivo: str
    payload_canonico: dict[str, Any] | None
    creator: uuid.UUID | None
    created_at: datetime
    confirmed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class ImportacionConfirmationResponse(ImportacionRead):
    @validator("confirmed_at")
    def confirmed_must_be_set(cls, v):
        if v is None:
            raise ValueError("La importación no está confirmada")
        return v