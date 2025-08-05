#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chango_ADM - Backend API
MVP Sistema de Gestión de Empleados con FastAPI
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn
from datetime import datetime, timedelta

# Importar módulos del proyecto
from database.connection import get_db
from models.empleado import Empleado, EmpleadoCreate, EmpleadoUpdate
from models.usuario import Usuario, UsuarioCreate, UsuarioLogin
from models.fichaje import Fichaje, FichajeCreate
from models.recibo import ReciboSueldo, ReciboCreate
from services.auth_service import AuthService
from services.empleado_service import EmpleadoService
from services.fichaje_service import FichajeService
from services.recibo_service import ReciboService

# Configuración de la aplicación
app = FastAPI(
    title="Chango_ADM API",
    description="API para Sistema de Gestión de Empleados - MVP",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servicios
auth_service = AuthService()
empleado_service = EmpleadoService()
fichaje_service = FichajeService()
recibo_service = ReciboService()

# =====================================================
# ENDPOINTS DE AUTENTICACIÓN
# =====================================================

@app.post("/auth/login", response_model=dict)
async def login(credentials: UsuarioLogin, db: Session = Depends(get_db)):
    """Login de usuario"""
    try:
        token = auth_service.authenticate_user(db, credentials.username, credentials.password)
        return {
            "access_token": token,
            "token_type": "bearer",
            "message": "Login exitoso"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

@app.post("/auth/register", response_model=dict)
async def register(user: UsuarioCreate, db: Session = Depends(get_db)):
    """Registro de nuevo usuario"""
    try:
        new_user = auth_service.create_user(db, user)
        return {
            "message": "Usuario creado exitosamente",
            "user_id": new_user.id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# =====================================================
# ENDPOINTS DE EMPLEADOS
# =====================================================

@app.get("/empleados", response_model=List[Empleado])
async def get_empleados(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth_service.get_current_user)
):
    """Obtener lista de empleados"""
    empleados = empleado_service.get_empleados(db, skip=skip, limit=limit)
    return empleados

@app.get("/empleados/{empleado_id}", response_model=Empleado)
async def get_empleado(
    empleado_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth_service.get_current_user)
):
    """Obtener empleado por ID"""
    empleado = empleado_service.get_empleado(db, empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado

@app.post("/empleados", response_model=Empleado)
async def create_empleado(
    empleado: EmpleadoCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth_service.get_current_user)
):
    """Crear nuevo empleado"""
    return empleado_service.create_empleado(db, empleado)

@app.put("/empleados/{empleado_id}", response_model=Empleado)
async def update_empleado(
    empleado_id: int, 
    empleado: EmpleadoUpdate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth_service.get_current_user)
):
    """Actualizar empleado"""
    updated_empleado = empleado_service.update_empleado(db, empleado_id, empleado)
    if not updated_empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return updated_empleado

# =====================================================
# ENDPOINTS DE FICHAJES (TAW)
# =====================================================

@app.post("/fichajes/entrada", response_model=Fichaje)
async def registrar_entrada(
    fichaje: FichajeCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth_service.get_current_user)
):
    """Registrar entrada de empleado"""
    return fichaje_service.registrar_entrada(db, fichaje)

@app.post("/fichajes/salida", response_model=Fichaje)
async def registrar_salida(
    fichaje: FichajeCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth_service.get_current_user)
):
    """Registrar salida de empleado"""
    return fichaje_service.registrar_salida(db, fichaje)

@app.get("/fichajes/empleado/{empleado_id}")
async def get_fichajes_empleado(
    empleado_id: int,
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth_service.get_current_user)
):
    """Obtener fichajes de un empleado"""
    return fichaje_service.get_fichajes_empleado(db, empleado_id, fecha_inicio, fecha_fin)

# =====================================================
# ENDPOINTS DE RECIBOS DE SUELDO
# =====================================================

@app.get("/recibos/empleado/{empleado_id}")
async def get_recibos_empleado(
    empleado_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth_service.get_current_user)
):
    """Obtener recibos de sueldo de un empleado"""
    return recibo_service.get_recibos_empleado(db, empleado_id)

@app.post("/recibos/generar", response_model=ReciboSueldo)
async def generar_recibo(
    recibo: ReciboCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth_service.get_current_user)
):
    """Generar recibo de sueldo"""
    return recibo_service.generar_recibo(db, recibo)

@app.post("/recibos/{recibo_id}/firmar")
async def firmar_recibo(
    recibo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth_service.get_current_user)
):
    """Firmar recibo de sueldo"""
    return recibo_service.firmar_recibo(db, recibo_id, current_user.id)

# =====================================================
# ENDPOINTS DE ESTADÍSTICAS
# =====================================================

@app.get("/stats/empleados")
async def get_stats_empleados(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth_service.get_current_user)
):
    """Obtener estadísticas de empleados"""
    return empleado_service.get_stats(db)

@app.get("/stats/fichajes")
async def get_stats_fichajes(
    fecha: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth_service.get_current_user)
):
    """Obtener estadísticas de fichajes"""
    return fichaje_service.get_stats(db, fecha)

# =====================================================
# ENDPOINTS DE SALUD
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
        "docs": "/docs"
    }

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