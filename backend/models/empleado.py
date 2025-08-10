from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EmpleadoBase(BaseModel):
    nombre: str
    apellido: str
    email: str
    telefono: Optional[str] = None
    departamento: str
    cargo: str
    salario: float
    fecha_contratacion: datetime

class EmpleadoCreate(EmpleadoBase):
    pass

class EmpleadoUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    departamento: Optional[str] = None
    cargo: Optional[str] = None
    salario: Optional[float] = None
    fecha_contratacion: Optional[datetime] = None

class Empleado(EmpleadoBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
