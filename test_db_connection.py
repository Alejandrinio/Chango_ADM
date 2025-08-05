#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar la conexión a la base de datos MySQL
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from backend.database.connection import engine, get_db
    from sqlalchemy import text
    
    print("🔌 Probando conexión a la base de datos...")
    
    # Probar conexión directa
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("✅ Conexión exitosa!")
        
        # Probar consulta a la base de datos
        result = connection.execute(text("SHOW TABLES"))
        tables = result.fetchall()
        print(f"📋 Tablas encontradas: {len(tables)}")
        
        for table in tables:
            print(f"   - {table[0]}")
            
        # Probar consulta de empleados
        result = connection.execute(text("SELECT COUNT(*) FROM empleados"))
        count = result.fetchone()[0]
        print(f"👥 Empleados en la base de datos: {count}")
        
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("💡 Asegúrate de tener instaladas las dependencias:")
    print("   pip install -r requirements.txt")
    
except Exception as e:
    print(f"❌ Error de conexión: {e}")
    print("💡 Verifica que:")
    print("   1. MySQL esté ejecutándose")
    print("   2. La base de datos 'chango_adm_db' exista")
    print("   3. Las credenciales sean correctas")

print("\n🎯 Prueba completada!") 