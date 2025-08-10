# 🚀 Chango_ADM - Sistema de Gestión RRHH

Sistema completo de gestión de recursos humanos con FastAPI backend y frontend moderno.

## 📋 Características

### ✅ **P0 - Crítico (MVP)**
- **Dashboard** con KPIs en tiempo real y gráficos interactivos
- **Gestión de Empleados** (ABM completo con búsqueda y exportación)
- **Control de Fichajes** con detección de anomalías y ajustes manuales
- **Recibos de Sueldo** con flujo completo de generación → firma → aprobación → publicación
- **API REST** completa con documentación automática

### 🔄 **P1 - Importante (Post-demo)**
- Gestión de Vacaciones
- Control de Horas Extras
- Configuración del Sistema
- Notificaciones

### 🚀 **P2 - Futuro**
- Integración con servicios externos (TAW, Walmart)
- IA para análisis predictivo
- Microservicios y contenedores
- Reportes avanzados

## 🛠️ Tecnologías

### Backend
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para base de datos
- **MySQL** - Base de datos principal
- **JWT** - Autenticación segura
- **Pydantic** - Validación de datos

### Frontend
- **HTML5/CSS3** - Interfaz moderna y responsive
- **JavaScript** - Interactividad y llamadas API
- **Bootstrap 4** - Framework CSS
- **Chart.js** - Gráficos interactivos
- **DataTables** - Tablas con paginación y filtros

## 🚀 Instalación Rápida

### Prerrequisitos
- Python 3.8+
- MySQL 8.0+
- Git

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd Chango_ADM
```

### 2. Setup automatizado
```bash
python setup.py
```

### 3. Iniciar servicios
```bash
# Terminal 1 - Backend
python main.py

# Terminal 2 - Frontend
cd frontend
python -m http.server 3000
```

### 4. Acceder al sistema
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🔑 Credenciales de Acceso

### Usuario Administrador
- **Username**: `admin`
- **Password**: `admin123`

### Usuarios de Prueba
- **Username**: `nombre.apellido` (ej: `agapito.miralles`)
- **Password**: `123456`

## 📊 Estructura del Proyecto

```
Chango_ADM/
├── 📁 frontend/                 # Interfaz de usuario
│   ├── 📄 index.html           # Dashboard principal
│   ├── 📄 empleados.html       # Gestión de empleados
│   ├── 📄 fichajes.html        # Control de fichajes
│   ├── 📄 recibos.html         # Recibos de sueldo
│   ├── 📁 js/                  # JavaScript
│   │   ├── 📄 dashboard.js     # Lógica del dashboard
│   │   └── 📄            # Servicios API
│   └── 📁 partials/            # Componentes reutilizables
│       └── 📄 sidebar.html     # Navegación lateral
├── 📄 main.py                  # Aplicación FastAPI principal
├── 📄 config.py                # Configuración del sistema
├── 📄 database_setup.sql       # Script de base de datos
├── 📄 import_data.py           # Importación de datos de prueba
├── 📄 setup.py                 # Setup automatizado
├── 📄 requirements.txt         # Dependencias Python
└── 📄 README.md                # Documentación
```

## 🔌 API Endpoints

### Dashboard
- `GET /api/dashboard/kpis` - KPIs en tiempo real
- `GET /api/dashboard/charts` - Datos para gráficos

### Empleados
- `GET /api/empleados` - Lista con paginación y filtros
- `GET /api/empleados/{id}` - Detalle de empleado
- `POST /api/empleados` - Crear empleado
- `PUT /api/empleados/{id}` - Actualizar empleado
- `DELETE /api/empleados/{id}` - Baja lógica
- `GET /api/empleados/export` - Exportar a CSV

### Fichajes
- `GET /api/fichajes` - Lista con filtros
- `PATCH /api/fichajes/{id}` - Ajustar fichaje
- `GET /api/fichajes/export` - Exportar a CSV

### Recibos
- `GET /api/recibos` - Lista con filtros
- `POST /api/recibos/generar` - Generar recibo
- `POST /api/recibos/{id}/firmar` - Firmar recibo
- `POST /api/recibos/{id}/aprobar` - Aprobar recibo
- `POST /api/recibos/{id}/publicar` - Publicar recibo
- `GET /api/recibos/{id}/descargar` - Descargar recibo

## 🗄️ Base de Datos

### Tablas Principales
- **empleados** - Datos de empleados
- **usuarios** - Usuarios del sistema
- **fichajes** - Registro de asistencia
- **recibos_sueldo** - Recibos de sueldo
- **departamentos** - Departamentos de la empresa
- **vacaciones** - Solicitudes de vacaciones
- **horas_extras** - Control de horas extras
- **notificaciones** - Sistema de notificaciones

### Vistas Útiles
- **empleados_activos** - Empleados en estado activo
- **estadisticas_fichajes** - Estadísticas de asistencia

## 🎯 Funcionalidades por Rol

### 👑 Administrador
- Acceso total al sistema
- Gestión de usuarios y roles
- Configuración del sistema

### 👥 RRHH
- Gestión completa de empleados
- Aprobación de fichajes y recibos
- Reportes y estadísticas

### 👨‍💼 Supervisor
- Gestión de fichajes del equipo
- Aprobación de recibos
- Control de horas extras

### 👤 Empleado
- Ver fichajes propios
- Firmar recibos propios
- Solicitar vacaciones

## 🔧 Configuración

### Variables de Entorno
```bash
# Base de datos
DATABASE_URL=mysql+mysqlconnector://root:@localhost:3306/chango_adm_db

# Seguridad
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]
```

### Configuración de Desarrollo
```python
DEBUG = True
RELOAD = True
HOST = "0.0.0.0"
PORT = 8000
```

## 🧪 Testing

### Probar API
```bash
# Health check
curl http://localhost:8000/health

# Test database
curl http://localhost:8000/test-db

# Dashboard KPIs
curl http://localhost:8000/api/dashboard/kpis
```

### Probar Frontend
1. Abrir http://localhost:3000
2. Verificar que el dashboard cargue correctamente
3. Probar navegación entre páginas
4. Verificar que los gráficos se rendericen

## 🚀 Despliegue

### Desarrollo Local
```bash
# Backend con auto-reload
python main.py

# Frontend
cd frontend && python -m http.server 3000
```

### Producción (Futuro)
```bash
# Con Docker
docker-compose up -d

# Con Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 📈 Roadmap

### ✅ Completado (P0)
- [x] Dashboard con KPIs y gráficos
- [x] CRUD completo de empleados
- [x] Sistema de fichajes con anomalías
- [x] Flujo completo de recibos
- [x] API REST documentada

### 🔄 En Desarrollo (P1)
- [ ] Gestión de vacaciones
- [ ] Control de horas extras
- [ ] Sistema de notificaciones
- [ ] Configuración avanzada

### 🚀 Futuro (P2)
- [ ] Integración con TAW/Walmart
- [ ] IA para análisis predictivo
- [ ] Microservicios con Docker
- [ ] Reportes PDF avanzados
- [ ] App móvil

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

- **Email**: soporte@chango-adm.com
- **Documentación**: http://localhost:8000/docs
- **Issues**: GitHub Issues

## 🙏 Agradecimientos

- FastAPI por el excelente framework
- Bootstrap por el diseño responsive
- Chart.js por los gráficos interactivos
- MySQL por la base de datos robusta

---

**Chango_ADM** - Sistema de Gestión RRHH Moderno y Escalable 🚀
