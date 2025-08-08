from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FichajeBase(BaseModel):
    empleado_id: int
    tipo: str  # "entrada" o "salida"
    fecha_hora: datetime

class FichajeCreate(FichajeBase):
    pass

class Fichaje(FichajeBase):
    id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True
