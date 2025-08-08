from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from models.fichaje import Fichaje, FichajeCreate

class FichajeService:
    def registrar_entrada(self, db: Session, fichaje: FichajeCreate) -> Fichaje:
        """Registrar entrada de empleado"""
        # Simulación - en producción insertar en base de datos
        new_fichaje = Fichaje(
            id=1,
            empleado_id=fichaje.empleado_id,
            tipo="entrada",
            fecha_hora=fichaje.fecha_hora,
            fecha_creacion=datetime.utcnow()
        )
        return new_fichaje

    def registrar_salida(self, db: Session, fichaje: FichajeCreate) -> Fichaje:
        """Registrar salida de empleado"""
        # Simulación - en producción insertar en base de datos
        new_fichaje = Fichaje(
            id=2,
            empleado_id=fichaje.empleado_id,
            tipo="salida",
            fecha_hora=fichaje.fecha_hora,
            fecha_creacion=datetime.utcnow()
        )
        return new_fichaje

    def get_fichajes_empleado(self, db: Session, empleado_id: int, fecha_inicio: Optional[str] = None, fecha_fin: Optional[str] = None) -> List[Fichaje]:
        """Obtener fichajes de un empleado"""
        # Simulación de datos - en producción consultar base de datos
        fichajes = []
        for i in range(10):  # Simular 10 fichajes
            fichaje = Fichaje(
                id=i + 1,
                empleado_id=empleado_id,
                tipo="entrada" if i % 2 == 0 else "salida",
                fecha_hora=datetime.utcnow(),
                fecha_creacion=datetime.utcnow()
            )
            fichajes.append(fichaje)
        return fichajes
