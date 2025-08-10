#!/usr/bin/env python3
"""
Chango_ADM - Script de Setup Automatizado
Configura e instala el sistema completo
"""

import os
import sys
import subprocess
import mysql.connector
from pathlib import Path

def check_python_version():
    """Verificar versión de Python"""
    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def check_mysql():
    """Verificar conexión a MySQL"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        connection.close()
        print("✅ MySQL - Conexión exitosa")
        return True
    except mysql.connector.Error as err:
        print(f"❌ Error conectando a MySQL: {err}")
        print("   Asegúrate de que MySQL esté instalado y ejecutándose")
        return False

def install_dependencies():
    """Instalar dependencias de Python"""
    print("\n📦 Instalando dependencias...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def setup_database():
    """Configurar base de datos"""
    print("\n🗄️ Configurando base de datos...")
    
    # Verificar si existe el archivo SQL
    if not Path("database_setup.sql").exists():
        print("❌ Error: No se encontró database_setup.sql")
        return False
    
    try:
        # Ejecutar script SQL
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        cursor = connection.cursor()
        
        # Leer y ejecutar script SQL
        with open("database_setup.sql", "r", encoding="utf-8") as file:
            sql_script = file.read()
            
        # Dividir en comandos individuales
        commands = sql_script.split(';')
        
        for command in commands:
            command = command.strip()
            if command and not command.startswith('--'):
                try:
                    cursor.execute(command)
                except mysql.connector.Error as e:
                    if "already exists" not in str(e).lower():
                        print(f"⚠️ Advertencia SQL: {e}")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("✅ Base de datos configurada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error configurando base de datos: {e}")
        return False

def import_data():
    """Importar datos de prueba"""
    print("\n📥 Importando datos de prueba...")
    
    if not Path("Base_de_Datos_de_Empleados_MVP.csv").exists():
        print("⚠️ Advertencia: No se encontró Base_de_Datos_de_Empleados_MVP.csv")
        print("   Los datos de prueba no se importarán")
        return True
    
    try:
        subprocess.check_call([sys.executable, "import_data.py"])
        print("✅ Datos importados exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error importando datos: {e}")
        return False

def create_directories():
    """Crear directorios necesarios"""
    print("\n📁 Creando directorios...")
    
    directories = [
        "uploads",
        "reportes",
        "logs",
        "temp"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   ✅ {directory}/")
    
    return True

def test_backend():
    """Probar el backend"""
    print("\n🧪 Probando backend...")
    
    try:
        # Importar y probar configuración
        import config
        print("   ✅ Configuración cargada")
        
        # Probar conexión a BD
        import mysql.connector
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="chango_adm_db"
        )
        connection.close()
        print("   ✅ Conexión a BD exitosa")
        
        print("✅ Backend listo")
        return True
        
    except Exception as e:
        print(f"❌ Error probando backend: {e}")
        return False

def show_next_steps():
    """Mostrar próximos pasos"""
    print("\n🎉 ¡Setup completado exitosamente!")
    print("\n📋 PRÓXIMOS PASOS:")
    print("1. Iniciar el backend:")
    print("   python main.py")
    print("\n2. Iniciar el frontend (en otra terminal):")
    print("   cd frontend")
    print("   python -m http.server 3000")
    print("\n3. Acceder al sistema:")
    print("   Frontend: http://localhost:3000")
    print("   Backend API: http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")
    print("\n🔑 CREDENCIALES:")
    print("   Admin: admin / admin123")
    print("   Otros: nombre.apellido / 123456")
    print("\n📚 DOCUMENTACIÓN:")
    print("   - API Docs: http://localhost:8000/docs")
    print("   - README.md para más información")

def main():
    """Función principal"""
    print("🚀 Chango_ADM - Setup Automatizado")
    print("=" * 50)
    
    # Verificaciones iniciales
    if not check_python_version():
        return False
    
    if not check_mysql():
        return False
    
    # Instalación y configuración
    if not install_dependencies():
        return False
    
    if not setup_database():
        return False
    
    if not create_directories():
        return False
    
    if not test_backend():
        return False
    
    # Importar datos (opcional)
    import_data()
    
    # Mostrar próximos pasos
    show_next_steps()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
