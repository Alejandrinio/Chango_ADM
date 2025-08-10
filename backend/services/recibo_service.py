from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from models.recibo import ReciboSueldo, ReciboCreate

class ReciboService:
    def get_recibos_empleado(self, db: Session, empleado_id: int) -> List[ReciboSueldo]:
        """Obtener recibos de sueldo de un empleado"""
        # Simulación de datos - en producción consultar base de datos
        recibos = []
        for i in range(12):  # Simular 12 meses de recibos
            recibo = ReciboSueldo(
                id=i + 1,
                empleado_id=empleado_id,
                mes=i + 1,
                año=2024,
                salario_bruto=30000.0,
                salario_neto=25000.0,
                fecha_generacion=datetime.utcnow(),
                firmado=i > 6,  # Los últimos 6 meses firmados
                fecha_firma=datetime.utcnow() if i > 6 else None
            )
            recibos.append(recibo)
        return recibos

    def generar_recibo(self, db: Session, recibo: ReciboCreate) -> ReciboSueldo:
        """Generar nuevo recibo de sueldo"""
        # Simulación - en producción insertar en base de datos
        new_recibo = ReciboSueldo(
            id=999,
            empleado_id=recibo.empleado_id,
            mes=recibo.mes,
            año=recibo.año,
            salario_bruto=recibo.salario_bruto,
            salario_neto=recibo.salario_neto,
            fecha_generacion=recibo.fecha_generacion,
            firmado=False,
            fecha_firma=None
        )
        return new_recibo

    def firmar_recibo(self, db: Session, recibo_id: int) -> ReciboSueldo:
        """Firmar un recibo de sueldo"""
        # Simulación - en producción actualizar en base de datos
        recibo = ReciboSueldo(
            id=recibo_id,
            empleado_id=1,
            mes=12,
            año=2024,
            salario_bruto=30000.0,
            salario_neto=25000.0,
            fecha_generacion=datetime.utcnow(),
            firmado=True,
            fecha_firma=datetime.utcnow()
        )
        return recibo
