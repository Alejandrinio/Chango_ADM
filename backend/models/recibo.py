from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReciboBase(BaseModel):
    empleado_id: int
    mes: int
    año: int
    salario_bruto: float
    salario_neto: float
    fecha_generacion: datetime

class ReciboCreate(ReciboBase):
    pass

class ReciboSueldo(ReciboBase):
    id: int
    firmado: bool = False
    fecha_firma: Optional[datetime] = None

    class Config:
        from_attributes = True
