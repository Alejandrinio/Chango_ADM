"""
Configuración centralizada para Chango_ADM
Sistema de Gestión RRHH
"""

import os
from typing import List

# Configuración de la Base de Datos
DATABASE_URL = "mysql+mysqlconnector://root:@localhost:3306/chango_adm_db"

# Configuración de Seguridad
SECRET_KEY = "chango_adm_secret_key_2024_very_secure_for_production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuración CORS
CORS_ORIGINS: List[str] = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

# Configuración de Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Configuración de Paginación
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

# Configuración de Archivos
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Configuración de Email (futuro)
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = ""
SMTP_PASSWORD = ""

# Configuración de Redis (futuro para cache)
REDIS_URL = "redis://localhost:6379"

# Configuración de IA (futuro)
AI_SERVICE_URL = "http://localhost:5000"

# Configuración de Integraciones Externas
TAW_API_URL = "https://api.taw.com"  # Placeholder
WALMART_API_URL = "https://api.walmart.com"  # Placeholder

# Configuración de Horarios Laborales
HORARIOS_DEFAULT = {
    "lunes_viernes": "09:00-18:00",
    "sabado": "09:00-13:00",
    "domingo": "Cerrado"
}

# Configuración de Estados
ESTADOS_EMPLEADO = ["activo", "inactivo", "vacaciones", "licencia"]
ESTADOS_RECIBO = ["generado", "firmado", "aprobado", "publicado"]
ESTADOS_FICHAJE = ["normal", "tardanza", "salida_temprana", "ausencia", "ajustado"]

# Configuración de Roles
ROLES_SISTEMA = ["admin", "rrhh", "supervisor", "empleado"]

# Configuración de Notificaciones
NOTIFICACIONES_EMAIL = True
NOTIFICACIONES_PUSH = False

# Configuración de Reportes
REPORTES_DIR = "reportes"
FORMATOS_REPORTE = ["pdf", "csv", "excel"]

# Configuración de Auditoría
AUDITORIA_HABILITADA = True
AUDITORIA_TABLAS = ["empleados", "fichajes", "recibos_sueldo", "usuarios"]

# Configuración de Backup
BACKUP_AUTOMATICO = True
BACKUP_FRECUENCIA = "daily"  # daily, weekly, monthly
BACKUP_RETENCION = 30  # días

# Configuración de Performance
CACHE_TTL = 300  # 5 minutos
QUERY_TIMEOUT = 30  # segundos
MAX_CONNECTIONS = 20

# Configuración de Desarrollo
DEBUG = True
RELOAD = True
HOST = "0.0.0.0"
PORT = 8000

# Configuración de Testing
TESTING = False
TEST_DATABASE_URL = "mysql+mysqlconnector://root:@localhost:3306/chango_adm_test"

# Configuración de Monitoreo
HEALTH_CHECK_ENABLED = True
METRICS_ENABLED = True
