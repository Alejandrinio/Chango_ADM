# -*- coding: utf-8 -*-
"""
Configuración del proyecto Chango_ADM
"""

import os
from datetime import timedelta
from typing import Optional

# Configuración de la base de datos
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+mysqlconnector://root:@localhost:3306/chango_adm_db"
)

# Configuración de la aplicación
APP_NAME = "Chango_ADM API"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "API para Sistema de Gestión de Empleados - MVP"

# Configuración de seguridad
SECRET_KEY = os.getenv("SECRET_KEY", "chango_adm_secret_key_2024_mvp")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuración de CORS
CORS_ORIGINS = [
    "http://localhost:3000",  # React
    "http://localhost:8080",  # Vue
    "http://localhost:4200",  # Angular
    "*"  # Para desarrollo
]

# Configuración de logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Configuración de paginación
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Configuración de archivos
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Configuración de email (futuro)
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

# Configuración de IA (futuro)
AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://localhost:8001")
AI_SERVICE_TIMEOUT = int(os.getenv("AI_SERVICE_TIMEOUT", "30"))

# Configuración de Redis (futuro)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Configuración de sueldos base por rol
SALARY_BASE = {
    'Cajero': 1200.00,
    'Repositor': 1100.00,
    'Mantenimiento': 1300.00,
    'Seguridad': 1250.00,
    'Gerente': 2500.00,
    'Soporte Técnico': 1800.00,
    'Analista RRHH': 1600.00,
    'Administrativo': 1400.00,
    'Secretaria': 1200.00,
    'Operaciones y Logística': 1500.00,
    'Infraestructura': 1700.00,
    'Marketing': 1600.00,
    'RRHH': 1500.00
}

# Configuración de horas extras
OVERTIME_RATES = {
    '50%': 1.5,
    '100%': 2.0
} 