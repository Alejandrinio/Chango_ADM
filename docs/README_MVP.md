# 🚀 Chango_ADM - MVP Sistema de Gestión de Empleados

## 📋 Descripción del Proyecto

Este es un **MVP (Minimum Viable Product)** para un sistema de gestión de empleados que integra servicios de **Walmart** y **TAW** (herramienta de fichaje). El sistema permite gestionar empleados, fichajes, horas extras y recibos de sueldo.

## 🎯 Funcionalidades del MVP

### Primera Instancia
- ✅ **Plataforma de entrada/login** - Sistema de autenticación
- ✅ **Dashboard principal** - Panel de control con todas las herramientas
- ✅ **Herramienta de TAW** - Fichaje, entrada y salida
- ✅ **Estimación de horas** - Cálculo automático para pagos

### Segunda Instancia
- ✅ **Recibo de sueldo** - Generación y gestión
- ✅ **Firma y aprobación** - Flujo de aprobación de recibos

## 🛠️ Tecnologías Utilizadas

### Frontend
- **HTML5** - Estructura de páginas
- **CSS3** - Estilos y diseño responsive
- **JavaScript** - Interactividad
- **Bootstrap 4** - Framework CSS
- **jQuery** - Biblioteca JavaScript
- **DataTables** - Tablas interactivas
- **Flot Charts** - Gráficos y estadísticas

### Backend
- **Python 3.8+** - Lenguaje principal
- **Flask** - Framework web
- **MySQL** - Base de datos
- **MySQL Connector** - Conector de base de datos

## 📦 Instalación y Configuración

### 1. Prerrequisitos

- **Python 3.8 o superior**
- **MySQL 8.0 o superior**
- **MySQL Workbench** (opcional, para gestión visual)

### 2. Clonar el Proyecto

```bash
git clone <url-del-repositorio>
cd Chango_ADM
```

### 3. Configurar Base de Datos

#### Opción A: Usando MySQL Workbench
1. Abrir MySQL Workbench
2. Conectar a tu servidor MySQL
3. Ejecutar el script `database_setup.sql`
4. Verificar que se creó la base de datos `chango_adm_db`

#### Opción B: Usando línea de comandos
```bash
mysql -u root -p < database_setup.sql
```

### 4. Configurar Credenciales

Editar el archivo `config.py` y `import_csv_to_mysql.py` con tus credenciales de MySQL:

```python
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'tu_usuario',      # Cambiar
    'password': 'tu_password', # Cambiar
    'database': 'chango_adm_db',
    'charset': 'utf8mb4'
}
```

### 5. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 6. Importar Datos del CSV

```bash
python import_csv_to_mysql.py
```

Este script:
- Importa todos los empleados del CSV
- Genera usuarios de login automáticamente
- Crea datos de fichaje de los últimos 30 días
- Genera recibos de sueldo del mes actual

### 7. Levantar el Servidor

```bash
python -m http.server 8000
```

Acceder a: http://localhost:8000

## 📊 Estructura de la Base de Datos

### Tablas Principales

1. **empleados** - Información básica de empleados
2. **usuarios** - Credenciales de login
3. **fichajes** - Registro de entrada/salida (TAW)
4. **horas_extras** - Control de horas extras
5. **recibos_sueldo** - Recibos de sueldo
6. **departamentos** - Departamentos de la empresa
7. **vacaciones** - Solicitudes de vacaciones
8. **notificaciones** - Sistema de notificaciones

### Vistas Útiles

- **empleados_activos** - Solo empleados activos
- **resumen_fichajes_diarios** - Resumen de fichajes

## 🔐 Credenciales de Acceso

### Usuarios Generados Automáticamente

El sistema genera automáticamente usuarios basados en los datos del CSV:

- **Username**: `nombreapellido123` (ej: `agapitomiralles123`)
- **Password**: `password` (para todos los usuarios)
- **Roles**: Se asignan automáticamente según el cargo

### Roles del Sistema

- **admin** - Acceso completo al sistema
- **gerente** - Gestión de empleados y aprobaciones
- **supervisor** - Gestión de equipo
- **empleado** - Acceso básico

## 📱 Páginas Principales

### Autenticación
- `/authentication-login.html` - Página de login
- `/authentication-register.html` - Registro (futuro)

### Dashboard
- `/index.html` - Dashboard principal
- `/index2.html` - Dashboard alternativo con calendario

### Gestión de Empleados
- `/tables.html` - Lista de empleados
- `/form-basic.html` - Formularios de empleados

### Reportes
- `/charts.html` - Gráficos y estadísticas
- `/widgets.html` - Widgets informativos

## 🔧 Configuración Avanzada

### Variables de Entorno

Crear archivo `.env`:

```env
MYSQL_HOST=localhost
MYSQL_USER=tu_usuario
MYSQL_PASSWORD=tu_password
MYSQL_DATABASE=chango_adm_db
SECRET_KEY=tu_clave_secreta
DEBUG=True
```

### Configuración de Logs

Los logs se guardan en `logs/chango_adm.log`

### Configuración de Backup

El sistema incluye configuración para backups automáticos en `backups/`

## 📈 Datos de Ejemplo Generados

### Empleados
- **100+ empleados** importados del CSV
- **Datos completos**: nombre, apellido, domicilio, fecha nacimiento, etc.
- **Emails y teléfonos** generados automáticamente

### Fichajes
- **30 días de fichajes** para cada empleado
- **Horarios realistas**: entrada 8-9:30, salida 17-19
- **Solo días laborables** (lunes a viernes)

### Recibos de Sueldo
- **Sueldos base** según rol del empleado
- **Horas extras** calculadas automáticamente
- **Bonificaciones y descuentos** simulados

## 🚀 Próximos Pasos

### Funcionalidades Futuras
- [ ] **API REST** para integración con Walmart
- [ ] **Webhooks** para sincronización con TAW
- [ ] **Sistema de notificaciones** por email
- [ ] **Reportes avanzados** en PDF/Excel
- [ ] **App móvil** para fichaje
- [ ] **Dashboard en tiempo real**

### Mejoras Técnicas
- [ ] **Autenticación JWT**
- [ ] **API rate limiting**
- [ ] **Caché Redis**
- [ ] **Docker containerization**
- [ ] **CI/CD pipeline**

## 🐛 Solución de Problemas

### Error de Conexión MySQL
```bash
# Verificar que MySQL esté corriendo
sudo service mysql status

# Verificar credenciales
mysql -u root -p
```

### Error de Dependencias
```bash
# Actualizar pip
pip install --upgrade pip

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### Error de Permisos
```bash
# Dar permisos de escritura
chmod 755 logs/
chmod 755 backups/
```

## 📞 Soporte

Para soporte técnico o consultas:
- **Email**: soporte@chango-adm.com
- **Documentación**: [Wiki del proyecto]
- **Issues**: [GitHub Issues]

## 📄 Licencia

Este proyecto es propiedad de la empresa y está destinado para uso interno.

---

**Desarrollado con ❤️ para el MVP de Chango_ADM** 