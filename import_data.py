"""
Chango_ADM - Script de Importación de Datos
Importa datos del CSV y genera datos de prueba para el sistema
"""

import mysql.connector
import csv
import random
from datetime import datetime, timedelta
import hashlib
import config

def hash_password(password):
    """Generar hash de contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

def generar_datos_fantasia(rol):
    """Generar datos de fantasía basados en el rol"""
    sueldos_base = {
        'Cajero': 45000,
        'Repositor': 42000,
        'Mantenimiento': 48000,
        'Supervisor': 65000,
        'Gerente': 85000,
        'Administrativo': 55000
    }
    
    return {
        'sueldo_base': sueldos_base.get(rol, 45000),
        'horas_extras': random.randint(0, 20),
        'sueldo_neto': sueldos_base.get(rol, 45000) + random.randint(0, 5000)
    }

def conectar_db():
    """Conectar a la base de datos"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="chango_adm_db"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error conectando a la base de datos: {err}")
        return None

def importar_empleados_desde_csv():
    """Importar empleados desde el archivo CSV"""
    connection = conectar_db()
    if not connection:
        return False
    
    cursor = connection.cursor()
    
    try:
        # Leer archivo CSV
        with open('Base_de_Datos_de_Empleados_MVP.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                # Asignar departamento aleatorio
                departamento_id = random.randint(1, 6)
                
                # Insertar empleado
                empleado_query = """
                INSERT INTO empleados (
                    nombre, apellido, domicilio, fecha_nacimiento, nivel_estudio,
                    rol, horario_laboral, email, telefono, fecha_ingreso, departamento_id, estado
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """
                
                empleado_data = (
                    row['Nombre'],
                    row['Apellido'],
                    row['Domicilio'],
                    row['Fecha de Nacimiento'],
                    row['Nivel de Estudio'],
                    row['Rol'],
                    row['Horario Laboral'],
                    row['Email'],
                    row['Telefono'],
                    row['Fecha de Ingreso'],
                    departamento_id,
                    'activo'
                )
                
                cursor.execute(empleado_query, empleado_data)
                empleado_id = cursor.lastinsertid
                
                # Crear usuario para el empleado
                username = f"{row['Nombre'].lower()}.{row['Apellido'].lower()}"
                password_hash = hash_password('123456')
                
                usuario_query = """
                INSERT INTO usuarios (username, password_hash, empleado_id, rol_sistema)
                VALUES (%s, %s, %s, %s)
                """
                
                # Asignar rol de sistema basado en el rol del empleado
                rol_sistema = 'empleado'
                if 'gerente' in row['Rol'].lower() or 'supervisor' in row['Rol'].lower():
                    rol_sistema = 'supervisor'
                elif 'rrhh' in row['Rol'].lower():
                    rol_sistema = 'rrhh'
                
                usuario_data = (username, password_hash, empleado_id, rol_sistema)
                cursor.execute(usuario_query, usuario_data)
                
                # Generar fichajes de los últimos 30 días
                generar_fichajes_empleado(cursor, empleado_id, row['Rol'])
                
                # Generar recibos de sueldo de los últimos 3 meses
                generar_recibos_empleado(cursor, empleado_id, row['Rol'])
        
        connection.commit()
        print("✅ Empleados importados exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error importando empleados: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()

def generar_fichajes_empleado(cursor, empleado_id, rol):
    """Generar fichajes de fantasía para un empleado"""
    fecha_inicio = datetime.now() - timedelta(days=30)
    
    for i in range(30):
        fecha = fecha_inicio + timedelta(days=i)
        
        # Saltar fines de semana
        if fecha.weekday() >= 5:  # Sábado = 5, Domingo = 6
            continue
        
        # Generar horarios de entrada y salida
        hora_entrada = datetime.strptime('09:00', '%H:%M').time()
        hora_salida = datetime.strptime('18:00', '%H:%M').time()
        
        # Agregar variabilidad
        if random.random() < 0.1:  # 10% de tardanzas
            hora_entrada = (datetime.strptime('09:00', '%H:%M') + timedelta(minutes=random.randint(5, 30))).time()
        
        if random.random() < 0.05:  # 5% de salidas tempranas
            hora_salida = (datetime.strptime('18:00', '%H:%M') - timedelta(minutes=random.randint(15, 60))).time()
        
        # Calcular horas trabajadas
        entrada_dt = datetime.combine(fecha, hora_entrada)
        salida_dt = datetime.combine(fecha, hora_salida)
        horas_trabajadas = (salida_dt - entrada_dt).total_seconds() / 3600
        
        # Determinar estado
        estado = 'normal'
        if hora_entrada > datetime.strptime('09:00', '%H:%M').time():
            estado = 'tardanza'
        elif hora_salida < datetime.strptime('18:00', '%H:%M').time():
            estado = 'salida_temprana'
        
        # Insertar fichaje
        fichaje_query = """
        INSERT INTO fichajes (empleado_id, fecha, hora_entrada, hora_salida, horas_trabajadas, estado)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        fichaje_data = (
            empleado_id,
            fecha.date(),
            hora_entrada,
            hora_salida,
            round(horas_trabajadas, 2),
            estado
        )
        
        cursor.execute(fichaje_query, fichaje_data)

def generar_recibos_empleado(cursor, empleado_id, rol):
    """Generar recibos de sueldo de fantasía para un empleado"""
    datos_fantasia = generar_datos_fantasia(rol)
    
    # Generar recibos de los últimos 3 meses
    for i in range(3):
        fecha = datetime.now() - timedelta(days=30 * (i + 1))
        periodo = fecha.strftime('%Y-%m')
        
        recibo_query = """
        INSERT INTO recibos_sueldo (empleado_id, periodo, sueldo_base, horas_extras, sueldo_neto, estado)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        # Estado aleatorio
        estados = ['generado', 'firmado', 'aprobado', 'publicado']
        estado = random.choices(estados, weights=[0.3, 0.3, 0.2, 0.2])[0]
        
        recibo_data = (
            empleado_id,
            periodo,
            datos_fantasia['sueldo_base'],
            datos_fantasia['horas_extras'],
            datos_fantasia['sueldo_neto'],
            estado
        )
        
        cursor.execute(recibo_query, recibo_data)

def crear_usuario_admin():
    """Crear usuario administrador"""
    connection = conectar_db()
    if not connection:
        return False
    
    cursor = connection.cursor()
    
    try:
        # Crear empleado admin
        admin_query = """
        INSERT INTO empleados (
            nombre, apellido, domicilio, fecha_nacimiento, nivel_estudio,
            rol, horario_laboral, email, telefono, fecha_ingreso, departamento_id, estado
        ) VALUES (
            'Admin', 'Sistema', 'Dirección Admin', '1990-01-01', 'Universitario',
            'Administrador', 'Lunes a Viernes 9-18', 'admin@chango.com', '1234567890',
            '2024-01-01', 4, 'activo'
        )
        """
        
        cursor.execute(admin_query)
        admin_empleado_id = cursor.lastinsertid
        
        # Crear usuario admin
        admin_user_query = """
        INSERT INTO usuarios (username, password_hash, empleado_id, rol_sistema)
        VALUES ('admin', %s, %s, 'admin')
        """
        
        admin_user_data = (hash_password('admin123'), admin_empleado_id)
        cursor.execute(admin_user_query, admin_user_data)
        
        connection.commit()
        print("✅ Usuario administrador creado exitosamente")
        print("   Username: admin")
        print("   Password: admin123")
        return True
        
    except Exception as e:
        print(f"❌ Error creando usuario admin: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()

def mostrar_estadisticas():
    """Mostrar estadísticas de la base de datos"""
    connection = conectar_db()
    if not connection:
        return
    
    cursor = connection.cursor()
    
    try:
        # Contar empleados
        cursor.execute("SELECT COUNT(*) FROM empleados")
        total_empleados = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM empleados WHERE estado = 'activo'")
        empleados_activos = cursor.fetchone()[0]
        
        # Contar fichajes
        cursor.execute("SELECT COUNT(*) FROM fichajes")
        total_fichajes = cursor.fetchone()[0]
        
        # Contar recibos
        cursor.execute("SELECT COUNT(*) FROM recibos_sueldo")
        total_recibos = cursor.fetchone()[0]
        
        # Contar usuarios
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total_usuarios = cursor.fetchone()[0]
        
        print("\n📊 ESTADÍSTICAS DE LA BASE DE DATOS:")
        print("=" * 40)
        print(f"👥 Total empleados: {total_empleados}")
        print(f"✅ Empleados activos: {empleados_activos}")
        print(f"📅 Total fichajes: {total_fichajes}")
        print(f"💰 Total recibos: {total_recibos}")
        print(f"👤 Total usuarios: {total_usuarios}")
        
        # Mostrar distribución por roles
        cursor.execute("""
            SELECT rol, COUNT(*) as cantidad 
            FROM empleados 
            WHERE estado = 'activo' 
            GROUP BY rol 
            ORDER BY cantidad DESC
        """)
        
        print("\n🎭 DISTRIBUCIÓN POR ROLES:")
        print("-" * 30)
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]} empleados")
        
    except Exception as e:
        print(f"❌ Error obteniendo estadísticas: {e}")
    finally:
        cursor.close()
        connection.close()

def main():
    """Función principal"""
    print("🚀 Chango_ADM - Importación de Datos")
    print("=" * 50)
    
    # Verificar si existe el archivo CSV
    try:
        with open('Base_de_Datos_de_Empleados_MVP.csv', 'r', encoding='utf-8') as file:
            print("✅ Archivo CSV encontrado")
    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo 'Base_de_Datos_de_Empleados_MVP.csv'")
        print("   Asegúrate de que el archivo esté en el directorio raíz del proyecto")
        return
    
    # Crear usuario administrador
    print("\n👤 Creando usuario administrador...")
    if not crear_usuario_admin():
        return
    
    # Importar empleados
    print("\n📥 Importando empleados desde CSV...")
    if not importar_empleados_desde_csv():
        return
    
    # Mostrar estadísticas
    print("\n📈 Generando estadísticas...")
    mostrar_estadisticas()
    
    print("\n🎉 ¡Importación completada exitosamente!")
    print("\n🔑 CREDENCIALES DE ACCESO:")
    print("   Usuario Admin: admin / admin123")
    print("   Otros usuarios: nombre.apellido / 123456")
    print("\n🌐 URLs del sistema:")
    print("   Frontend: http://localhost:3000")
    print("   Backend API: http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
