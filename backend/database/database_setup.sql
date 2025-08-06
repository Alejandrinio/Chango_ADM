-- =====================================================
-- SCRIPT DE CONFIGURACIÓN DE BASE DE DATOS - MVP EMPRESA
-- VERSIÓN CORREGIDA PARA COMPATIBILIDAD
-- =====================================================

-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS chango_adm_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE chango_adm_db;

-- =====================================================
-- TABLA DE EMPLEADOS
-- =====================================================
CREATE TABLE empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    domicilio TEXT NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    nivel_estudio VARCHAR(50) NOT NULL,
    rol VARCHAR(100) NOT NULL,
    horario_laboral VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    telefono VARCHAR(20),
    fecha_ingreso DATE,
    estado ENUM('activo', 'inactivo', 'vacaciones', 'licencia') DEFAULT 'activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLA DE USUARIOS (para login)
-- =====================================================
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empleado_id INT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol_sistema ENUM('admin', 'gerente', 'supervisor', 'empleado') DEFAULT 'empleado',
    ultimo_login TIMESTAMP NULL,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE CASCADE
);

-- =====================================================
-- TABLA DE FICHAJES (TAW - Entrada/Salida)
-- =====================================================
CREATE TABLE fichajes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empleado_id INT NOT NULL,
    fecha DATE NOT NULL,
    hora_entrada TIME,
    hora_salida TIME,
    horas_trabajadas DECIMAL(4,2) DEFAULT 0,
    tipo ENUM('entrada', 'salida', 'pausa_inicio', 'pausa_fin') NOT NULL,
    ubicacion VARCHAR(255),
    dispositivo VARCHAR(100),
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE CASCADE,
    INDEX idx_empleado_fecha (empleado_id, fecha)
);

-- =====================================================
-- TABLA DE HORAS EXTRAS
-- =====================================================
CREATE TABLE horas_extras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empleado_id INT NOT NULL,
    fecha DATE NOT NULL,
    horas_extras DECIMAL(4,2) NOT NULL,
    tipo ENUM('50%', '100%') DEFAULT '50%',
    motivo TEXT,
    aprobado_por INT,
    estado ENUM('pendiente', 'aprobado', 'rechazado') DEFAULT 'pendiente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE CASCADE,
    FOREIGN KEY (aprobado_por) REFERENCES empleados(id)
);

-- =====================================================
-- TABLA DE RECIBOS DE SUELDO
-- =====================================================
CREATE TABLE recibos_sueldo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empleado_id INT NOT NULL,
    mes INT NOT NULL,
    año INT NOT NULL,
    sueldo_base DECIMAL(10,2) NOT NULL,
    horas_extras DECIMAL(10,2) DEFAULT 0,
    bonificaciones DECIMAL(10,2) DEFAULT 0,
    descuentos DECIMAL(10,2) DEFAULT 0,
    sueldo_neto DECIMAL(10,2) NOT NULL,
    fecha_generacion DATE,
    fecha_firma_empleado DATE NULL,
    fecha_aprobacion_supervisor DATE NULL,
    estado ENUM('generado', 'firmado', 'aprobado', 'pagado') DEFAULT 'generado',
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE CASCADE,
    UNIQUE KEY unique_empleado_mes_año (empleado_id, mes, año)
);

-- =====================================================
-- TABLA DE DEPARTAMENTOS
-- =====================================================
CREATE TABLE departamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    gerente_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (gerente_id) REFERENCES empleados(id)
);

-- =====================================================
-- TABLA DE VACACIONES
-- =====================================================
CREATE TABLE vacaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empleado_id INT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    dias_solicitados INT NOT NULL,
    motivo TEXT,
    estado ENUM('pendiente', 'aprobado', 'rechazado') DEFAULT 'pendiente',
    aprobado_por INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE CASCADE,
    FOREIGN KEY (aprobado_por) REFERENCES empleados(id)
);

-- =====================================================
-- TABLA DE NOTIFICACIONES
-- =====================================================
CREATE TABLE notificaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empleado_id INT NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    mensaje TEXT NOT NULL,
    tipo ENUM('info', 'warning', 'success', 'error') DEFAULT 'info',
    leida BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE CASCADE
);

-- =====================================================
-- INSERTAR DATOS DE EJEMPLO
-- =====================================================

-- Insertar algunos departamentos
INSERT INTO departamentos (nombre, descripcion) VALUES
('Ventas', 'Departamento de ventas y atención al cliente'),
('Operaciones', 'Departamento de operaciones y logística'),
('Recursos Humanos', 'Departamento de RRHH'),
('Mantenimiento', 'Departamento de mantenimiento'),
('Seguridad', 'Departamento de seguridad'),
('Administración', 'Departamento administrativo');

-- Crear índices para optimizar consultas
CREATE INDEX idx_empleados_rol ON empleados(rol);
CREATE INDEX idx_fichajes_fecha ON fichajes(fecha);
CREATE INDEX idx_recibos_mes_año ON recibos_sueldo(mes, año);
CREATE INDEX idx_usuarios_username ON usuarios(username);

-- Crear vista para empleados activos
CREATE VIEW empleados_activos AS
SELECT * FROM empleados WHERE estado = 'activo';

-- Crear vista para resumen de fichajes diarios
CREATE VIEW resumen_fichajes_diarios AS
SELECT 
    e.id,
    e.nombre,
    e.apellido,
    f.fecha,
    f.hora_entrada,
    f.hora_salida,
    f.horas_trabajadas
FROM empleados e
LEFT JOIN fichajes f ON e.id = f.empleado_id
WHERE e.estado = 'activo';

-- Mostrar mensaje de confirmación
SELECT 'Base de datos Chango_ADM creada exitosamente!' AS mensaje; 