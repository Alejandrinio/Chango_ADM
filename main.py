#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chango_ADM - Backend API
MVP Sistema de Gestión de Empleados con FastAPI
"""

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn
from datetime import datetime

# Importar solo lo que existe
from backend.database.connection import get_db
from backend.middleware.cors import setup_cors

# Configuración de la aplicación
app = FastAPI(
    title="Chango_ADM API",
    description="API para Sistema de Gestión de Empleados - MVP",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
setup_cors(app)

# =====================================================
# ENDPOINTS BÁSICOS
# =====================================================

@app.get("/health")
async def health_check():
    """Verificar estado de la API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "Chango_ADM API - Sistema de Gestión de Empleados",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "✅ Servidor funcionando correctamente"
    }

@app.get("/test-db")
async def test_database(db: Session = Depends(get_db)):
    """Probar conexión a la base de datos"""
    try:
        from sqlalchemy import text
        result = db.execute(text("SELECT COUNT(*) FROM empleados"))
        count = result.scalar()
        return {
            "status": "success",
            "message": "Conexión a base de datos exitosa",
            "empleados_count": count
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error de base de datos: {str(e)}"
        )

@app.get("/empleados-real")
async def get_empleados_real(db: Session = Depends(get_db)):
    """Obtener datos reales de empleados de la base de datos"""
    try:
        from sqlalchemy import text
        # Obtener los primeros 5 empleados con sus datos reales
        result = db.execute(text("""
            SELECT id, nombre, apellido, rol, horario_laboral, estado 
            FROM empleados 
            LIMIT 5
        """))
        empleados = []
        for row in result:
            empleados.append({
                "id": row[0],
                "nombre": row[1],
                "apellido": row[2],
                "rol": row[3],
                "horario_laboral": row[4],
                "estado": row[5]
            })
        
        # También obtener estadísticas
        count_result = db.execute(text("SELECT COUNT(*) FROM empleados"))
        total_count = count_result.scalar()
        
        return {
            "status": "success",
            "message": "Datos reales de la base de datos",
            "total_empleados": total_count,
            "muestra_empleados": empleados,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error de base de datos: {str(e)}"
        )

@app.get("/empleados-todos")
async def get_empleados_todos(
    limit: int = 20, 
    offset: int = 0, 
    db: Session = Depends(get_db)
):
    """Obtener todos los empleados con paginación"""
    try:
        from sqlalchemy import text
        # Obtener empleados con paginación
        result = db.execute(text("""
            SELECT id, nombre, apellido, rol, horario_laboral, estado, email, telefono
            FROM empleados 
            ORDER BY id
            LIMIT :limit OFFSET :offset
        """), {"limit": limit, "offset": offset})
        
        empleados = []
        for row in result:
            empleados.append({
                "id": row[0],
                "nombre": row[1],
                "apellido": row[2],
                "rol": row[3],
                "horario_laboral": row[4],
                "estado": row[5],
                "email": row[6],
                "telefono": row[7]
            })
        
        # Obtener total
        count_result = db.execute(text("SELECT COUNT(*) FROM empleados"))
        total_count = count_result.scalar()
        
        return {
            "status": "success",
            "message": f"Empleados {offset+1} a {offset+len(empleados)} de {total_count}",
            "total_empleados": total_count,
            "pagina_actual": offset // limit + 1,
            "empleados_por_pagina": limit,
            "empleados": empleados,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error de base de datos: {str(e)}"
        )

@app.get("/empleados/{empleado_id}")
async def get_empleado_por_id(empleado_id: int, db: Session = Depends(get_db)):
    """Obtener un empleado específico por ID"""
    try:
        from sqlalchemy import text
        result = db.execute(text("""
            SELECT id, nombre, apellido, rol, horario_laboral, estado, 
                   email, telefono, domicilio, fecha_nacimiento, nivel_estudio
            FROM empleados 
            WHERE id = :empleado_id
        """), {"empleado_id": empleado_id})
        
        row = result.fetchone()
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empleado con ID {empleado_id} no encontrado"
            )
        
        empleado = {
            "id": row[0],
            "nombre": row[1],
            "apellido": row[2],
            "rol": row[3],
            "horario_laboral": row[4],
            "estado": row[5],
            "email": row[6],
            "telefono": row[7],
            "domicilio": row[8],
            "fecha_nacimiento": str(row[9]) if row[9] else None,
            "nivel_estudio": row[10]
        }
        
        return {
            "status": "success",
            "empleado": empleado,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error de base de datos: {str(e)}"
        )

# =====================================================
# CONFIGURACIÓN DE EJECUCIÓN
# =====================================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 

@app.get("/api/empleados")
async def api_get_empleados(
    page: int = 1, 
    limit: int = 10, 
    search: str = None,
    db: Session = Depends(get_db)
):
    """API endpoint para el frontend - Lista de empleados con paginación y búsqueda"""
    try:
        from sqlalchemy import text
        
        offset = (page - 1) * limit
        
        # Construir query con búsqueda opcional
        if search:
            query = """
                SELECT id, nombre, apellido, rol, horario_laboral, estado, email, telefono
                FROM empleados 
                WHERE nombre LIKE :search OR apellido LIKE :search OR rol LIKE :search
                ORDER BY id
                LIMIT :limit OFFSET :offset
            """
            params = {"search": f"%{search}%", "limit": limit, "offset": offset}
        else:
            query = """
                SELECT id, nombre, apellido, rol, horario_laboral, estado, email, telefono
                FROM empleados 
                ORDER BY id
                LIMIT :limit OFFSET :offset
            """
            params = {"limit": limit, "offset": offset}
        
        result = db.execute(text(query), params)
        
        empleados = []
        for row in result:
            empleados.append({
                "id": row[0],
                "nombre": row[1],
                "apellido": row[2],
                "rol": row[3],
                "horario_laboral": row[4],
                "estado": row[5],
                "email": row[6],
                "telefono": row[7]
            })
        
        # Obtener total
        if search:
            count_query = """
                SELECT COUNT(*) FROM empleados 
                WHERE nombre LIKE :search OR apellido LIKE :search OR rol LIKE :search
            """
            count_params = {"search": f"%{search}%"}
        else:
            count_query = "SELECT COUNT(*) FROM empleados"
            count_params = {}
            
        count_result = db.execute(text(count_query), count_params)
        total_count = count_result.scalar()
        
        return {
            "success": True,
            "data": empleados,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total_count,
                "pages": (total_count + limit - 1) // limit
            },
            "search": search
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "data": []
        }

@app.get("/api/empleados/{empleado_id}")
async def api_get_empleado(empleado_id: int, db: Session = Depends(get_db)):
    """API endpoint para el frontend - Obtener empleado por ID"""
    try:
        from sqlalchemy import text
        result = db.execute(text("""
            SELECT id, nombre, apellido, rol, horario_laboral, estado, 
                   email, telefono, domicilio, fecha_nacimiento, nivel_estudio
            FROM empleados 
            WHERE id = :empleado_id
        """), {"empleado_id": empleado_id})
        
        row = result.fetchone()
        if not row:
            return {
                "success": False,
                "error": f"Empleado con ID {empleado_id} no encontrado"
            }
        
        empleado = {
            "id": row[0],
            "nombre": row[1],
            "apellido": row[2],
            "rol": row[3],
            "horario_laboral": row[4],
            "estado": row[5],
            "email": row[6],
            "telefono": row[7],
            "domicilio": row[8],
            "fecha_nacimiento": str(row[9]) if row[9] else None,
            "nivel_estudio": row[10]
        }
        
        return {
            "success": True,
            "data": empleado
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/api/stats")
async def api_get_stats(db: Session = Depends(get_db)):
    """API endpoint para el frontend - Estadísticas generales"""
    try:
        from sqlalchemy import text
        
        # Estadísticas de empleados
        stats_result = db.execute(text("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN estado = 'activo' THEN 1 END) as activos,
                COUNT(CASE WHEN estado = 'inactivo' THEN 1 END) as inactivos,
                COUNT(CASE WHEN estado = 'vacaciones' THEN 1 END) as vacaciones
            FROM empleados
        """))
        
        stats_row = stats_result.fetchone()
        
        # Estadísticas por rol
        roles_result = db.execute(text("""
            SELECT rol, COUNT(*) as cantidad
            FROM empleados 
            GROUP BY rol 
            ORDER BY cantidad DESC
        """))
        
        roles_stats = []
        for row in roles_result:
            roles_stats.append({
                "rol": row[0],
                "cantidad": row[1]
            })
        
        return {
            "success": True,
            "data": {
                "empleados": {
                    "total": stats_row[0],
                    "activos": stats_row[1],
                    "inactivos": stats_row[2],
                    "vacaciones": stats_row[3]
                },
                "roles": roles_stats
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        } 