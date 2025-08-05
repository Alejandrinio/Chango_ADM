# 🚀 Chango_ADM - Sistema de Gestión de Empleados

## 📋 Descripción

Sistema de gestión de empleados desarrollado con **FastAPI** y **MySQL**. Este MVP incluye funcionalidades para gestión de empleados, fichajes (TAW), recibos de sueldo y estadísticas.

## 🏗️ Estructura del Proyecto

```
Chango_ADM/
├── backend/                 # Backend FastAPI
│   ├── models/             # Modelos de datos
│   ├── services/           # Lógica de negocio
│   ├── database/           # Configuración de BD
│   └── config.py           # Configuración
├── database/               # Scripts de base de datos
│   ├── database_setup_fixed.sql
│   └── Base_de_Datos_de_Empleados_MVP.csv
├── docs/                   # Documentación
├── scripts/                # Scripts de utilidad
├── main.py                 # Aplicación principal
├── requirements.txt        # Dependencias
└── README.md              # Este archivo
```

## 🛠️ Tecnologías

- **Backend**: FastAPI + Python 3.8+
- **Base de Datos**: MySQL 8.0+
- **ORM**: SQLAlchemy
- **Autenticación**: JWT
- **Documentación**: Swagger/OpenAPI

## 🚀 Instalación

### 1. Prerrequisitos
- Python 3.8+
- MySQL 8.0+
- Git

### 2. Clonar el proyecto
```bash
git clone <url-del-repositorio>
cd Chango_ADM
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos
```bash
# Ejecutar en MySQL Workbench
mysql -u root -p < database/database_setup_fixed.sql
```

### 5. Configurar variables de entorno
Crear archivo `.env`:
```env
DATABASE_URL=mysql+mysqlconnector://root:@localhost:3306/chango_adm_db
SECRET_KEY=tu_clave_secreta
DEBUG=True
```

### 6. Ejecutar la aplicación
```bash
python main.py
```

## 📱 Endpoints Principales

### Autenticación
- `POST /auth/login` - Login de usuario
- `POST /auth/register` - Registro de usuario

### Empleados
- `GET /empleados` - Listar empleados
- `GET /empleados/{id}` - Obtener empleado
- `POST /empleados` - Crear empleado
- `PUT /empleados/{id}` - Actualizar empleado

### Fichajes (TAW)
- `POST /fichajes/entrada` - Registrar entrada
- `POST /fichajes/salida` - Registrar salida
- `GET /fichajes/empleado/{id}` - Fichajes de empleado

### Recibos de Sueldo
- `GET /recibos/empleado/{id}` - Recibos de empleado
- `POST /recibos/generar` - Generar recibo
- `POST /recibos/{id}/firmar` - Firmar recibo

### Estadísticas
- `GET /stats/empleados` - Estadísticas de empleados
- `GET /stats/fichajes` - Estadísticas de fichajes

## 🔐 Credenciales de Prueba

- **Usuario**: `agapitomiralles123`
- **Password**: `password`

## 📊 Base de Datos

El sistema incluye:
- **100 empleados** con datos reales
- **4,400 fichajes** (30 días de datos)
- **100 recibos de sueldo** del mes actual
- **6 departamentos** configurados

## 🎯 Funcionalidades

### ✅ Implementadas
- Autenticación JWT
- CRUD de empleados
- Sistema de fichajes
- Generación de recibos
- Estadísticas básicas

### 🚧 En Desarrollo
- Integración con IA
- Microservicios
- Frontend moderno
- Reportes avanzados

## 📖 Documentación API

Una vez ejecutada la aplicación, accede a:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🐳 Docker (Futuro)

```bash
# Construir imagen
docker build -t chango-adm .

# Ejecutar contenedor
docker run -p 8000:8000 chango-adm
```

## 🤖 Integración con IA

El proyecto está preparado para integración con:
- **OpenAI API**
- **Modelos locales** en contenedores
- **Microservicios** de IA

## 📞 Soporte

Para consultas o soporte técnico:
- **Email**: soporte@chango-adm.com
- **Issues**: [GitHub Issues]

---

**Desarrollado con ❤️ para el MVP de Chango_ADM**
