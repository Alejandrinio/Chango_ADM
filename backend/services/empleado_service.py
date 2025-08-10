from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from models.empleado import Empleado, EmpleadoCreate, EmpleadoUpdate

class EmpleadoService:
    def get_empleados(self, db: Session, skip: int = 0, limit: int = 100) -> List[Empleado]:
        """Obtener lista de empleados"""
        # Simulación de datos - en producción consultar base de datos
        empleados = []
        for i in range(skip, skip + limit):
            empleado = Empleado(
                id=i + 1,
                nombre=f"Empleado {i + 1}",
                apellido=f"Apellido {i + 1}",
                email=f"empleado{i + 1}@empresa.com",
                telefono=f"+34 600 {i + 1:06d}",
                departamento="Desarrollo",
                cargo="Desarrollador",
                salario=30000.0 + (i * 1000),
                fecha_contratacion=datetime.utcnow(),
                fecha_creacion=datetime.utcnow(),
                fecha_actualizacion=None
            )
            empleados.append(empleado)
        return empleados

    def get_empleado(self, db: Session, empleado_id: int) -> Optional[Empleado]:
        """Obtener empleado por ID"""
        # Simulación - en producción consultar base de datos
        if empleado_id > 0:
            return Empleado(
                id=empleado_id,
                nombre=f"Empleado {empleado_id}",
                apellido=f"Apellido {empleado_id}",
                email=f"empleado{empleado_id}@empresa.com",
                telefono=f"+34 600 {empleado_id:06d}",
                departamento="Desarrollo",
                cargo="Desarrollador",
                salario=30000.0 + (empleado_id * 1000),
                fecha_contratacion=datetime.utcnow(),
                fecha_creacion=datetime.utcnow(),
                fecha_actualizacion=None
            )
        return None

    def create_empleado(self, db: Session, empleado: EmpleadoCreate) -> Empleado:
        """Crear nuevo empleado"""
        # Simulación - en producción insertar en base de datos
        new_empleado = Empleado(
            id=999,
            nombre=empleado.nombre,
            apellido=empleado.apellido,
            email=empleado.email,
            telefono=empleado.telefono,
            departamento=empleado.departamento,
            cargo=empleado.cargo,
            salario=empleado.salario,
            fecha_contratacion=empleado.fecha_contratacion,
            fecha_creacion=datetime.utcnow(),
            fecha_actualizacion=None
        )
        return new_empleado

    def update_empleado(self, db: Session, empleado_id: int, empleado: EmpleadoUpdate) -> Optional[Empleado]:
        """Actualizar empleado"""
        # Simulación - en producción actualizar en base de datos
        existing_empleado = self.get_empleado(db, empleado_id)
        if existing_empleado:
            # Actualizar campos proporcionados
            if empleado.nombre:
                existing_empleado.nombre = empleado.nombre
            if empleado.apellido:
                existing_empleado.apellido = empleado.apellido
            if empleado.email:
                existing_empleado.email = empleado.email
            if empleado.telefono:
                existing_empleado.telefono = empleado.telefono
            if empleado.departamento:
                existing_empleado.departamento = empleado.departamento
            if empleado.cargo:
                existing_empleado.cargo = empleado.cargo
            if empleado.salario:
                existing_empleado.salario = empleado.salario
            if empleado.fecha_contratacion:
                existing_empleado.fecha_contratacion = empleado.fecha_contratacion
            
            existing_empleado.fecha_actualizacion = datetime.utcnow()
            return existing_empleado
        return None

    def get_stats(self, db: Session) -> dict:
        """Obtener estadísticas de empleados"""
        # Simulación de estadísticas
        return {
            "total_empleados": 100,
            "empleados_activos": 95,
            "empleados_inactivos": 5,
            "promedio_salario": 35000.0,
            "departamentos": {
                "Desarrollo": 30,
                "Marketing": 20,
                "Ventas": 25,
                "Recursos Humanos": 10,
                "Finanzas": 15
            }
        }
