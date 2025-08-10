"""
Chango_ADM - Analizador de Base de Datos
Analiza la estructura actual y la compara con la propuesta
"""

import mysql.connector
from mysql.connector import Error

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
    except Error as err:
        print(f"Error conectando a la base de datos: {err}")
        return None

def analizar_estructura():
    """Analizar la estructura actual de la base de datos"""
    connection = conectar_db()
    if not connection:
        return
    
    cursor = connection.cursor()
    
    try:
        print("🔍 ANALIZANDO ESTRUCTURA ACTUAL DE LA BASE DE DATOS")
        print("=" * 60)
        
        # Obtener todas las tablas
        cursor.execute("SHOW TABLES")
        tablas = [table[0] for table in cursor.fetchall()]
        
        print(f"\n📋 TABLAS ENCONTRADAS ({len(tablas)}):")
        for tabla in tablas:
            print(f"   ✅ {tabla}")
        
        # Analizar estructura de cada tabla
        for tabla in tablas:
            print(f"\n📊 ESTRUCTURA DE '{tabla}':")
            print("-" * 40)
            
            cursor.execute(f"DESCRIBE {tabla}")
            columnas = cursor.fetchall()
            
            for columna in columnas:
                nombre = columna[0]
                tipo = columna[1]
                null = columna[2]
                key = columna[3]
                default = columna[4]
                extra = columna[5]
                
                print(f"   {nombre:<20} {tipo:<15} {null:<3} {key:<3} {default or 'NULL':<10} {extra}")
        
        # Analizar vistas
        print(f"\n👁️ VISTAS ENCONTRADAS:")
        cursor.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW'")
        vistas = cursor.fetchall()
        
        for vista in vistas:
            print(f"   ✅ {vista[0]}")
        
        # Contar registros
        print(f"\n📈 ESTADÍSTICAS DE DATOS:")
        for tabla in tablas:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = cursor.fetchone()[0]
                print(f"   {tabla:<20}: {count:>5} registros")
            except:
                print(f"   {tabla:<20}: Error al contar")
        
        # Verificar datos de prueba
        print(f"\n🧪 VERIFICACIÓN DE DATOS:")
        
        # Empleados
        cursor.execute("SELECT COUNT(*) FROM empleados")
        total_empleados = cursor.fetchone()[0]
        print(f"   Empleados totales: {total_empleados}")
        
        if total_empleados > 0:
            cursor.execute("SELECT nombre, apellido, rol FROM empleados LIMIT 3")
            empleados_muestra = cursor.fetchall()
            print("   Muestra de empleados:")
            for emp in empleados_muestra:
                print(f"     - {emp[0]} {emp[1]} ({emp[2]})")
        
        # Fichajes
        cursor.execute("SELECT COUNT(*) FROM fichajes")
        total_fichajes = cursor.fetchone()[0]
        print(f"   Fichajes totales: {total_fichajes}")
        
        # Recibos
        cursor.execute("SELECT COUNT(*) FROM recibos_sueldo")
        total_recibos = cursor.fetchone()[0]
        print(f"   Recibos totales: {total_recibos}")
        
        # Usuarios
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total_usuarios = cursor.fetchone()[0]
        print(f"   Usuarios totales: {total_usuarios}")
        
        if total_usuarios > 0:
            cursor.execute("SELECT username, rol_sistema FROM usuarios LIMIT 3")
            usuarios_muestra = cursor.fetchall()
            print("   Muestra de usuarios:")
            for user in usuarios_muestra:
                print(f"     - {user[0]} ({user[1]})")
        
        print(f"\n✅ ANÁLISIS COMPLETADO")
        print(f"   La base de datos está lista para usar con la estructura actual")
        
    except Error as e:
        print(f"❌ Error analizando base de datos: {e}")
    finally:
        cursor.close()
        connection.close()

def verificar_compatibilidad():
    """Verificar compatibilidad con los endpoints propuestos"""
    print(f"\n🔧 VERIFICACIÓN DE COMPATIBILIDAD")
    print("=" * 50)
    
    connection = conectar_db()
    if not connection:
        return
    
    cursor = connection.cursor()
    
    try:
        # Verificar campos necesarios para endpoints
        endpoints_check = {
            "Dashboard KPIs": [
                "SELECT COUNT(*) FROM empleados WHERE estado = 'activo'",
                "SELECT COUNT(*) FROM fichajes WHERE fecha = CURDATE()"
            ],
            "Empleados CRUD": [
                "SELECT id, nombre, apellido, email, rol, estado FROM empleados LIMIT 1"
            ],
            "Fichajes": [
                "SELECT id, empleado_id, fecha, hora_entrada, hora_salida FROM fichajes LIMIT 1"
            ],
            "Recibos": [
                "SELECT id, empleado_id, sueldo_base, sueldo_neto, estado FROM recibos_sueldo LIMIT 1"
            ]
        }
        
        for endpoint, queries in endpoints_check.items():
            print(f"\n   🔍 {endpoint}:")
            for query in queries:
                try:
                    cursor.execute(query)
                    result = cursor.fetchone()
                    print(f"     ✅ Query ejecutada correctamente")
                except Error as e:
                    print(f"     ❌ Error: {e}")
        
        print(f"\n✅ VERIFICACIÓN COMPLETADA")
        
    except Error as e:
        print(f"❌ Error en verificación: {e}")
    finally:
        cursor.close()
        connection.close()

def main():
    """Función principal"""
    print("🚀 Chango_ADM - Analizador de Base de Datos")
    print("=" * 60)
    
    analizar_estructura()
    verificar_compatibilidad()
    
    print(f"\n🎯 RECOMENDACIONES:")
    print("   1. ✅ Usar la base de datos actual (no recrear)")
    print("   2. ✅ Adaptar endpoints a la estructura existente")
    print("   3. ✅ Mantener todos los datos reales")
    print("   4. ✅ Solo actualizar config.py y main.py")

if __name__ == "__main__":
    main()
