"""
Chango_ADM - Sistema de Gestión RRHH
FastAPI Backend Principal
"""

from fastapi import FastAPI, HTTPException, Depends, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy import create_engine, text, func, and_, or_
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import json
import csv
import io
from typing import List, Optional, Dict, Any
import config

# Crear aplicación FastAPI
app = FastAPI(
    title="Chango_ADM API",
    description="API para Sistema de Gestión RRHH",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar base de datos
engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency para obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================================================
# ENDPOINTS DE DASHBOARD (P0 - Crítico)
# ============================================================================

@app.get("/api/dashboard/kpis")
async def get_dashboard_kpis(
    fecha: Optional[str] = Query(None, description="Fecha en formato YYYY-MM-DD"),
    db = Depends(get_db)
):
    """Obtener KPIs del dashboard"""
    try:
        # Empleados activos (todos los empleados están activos)
        empleados_activos = db.execute(
            text("SELECT COUNT(*) FROM empleados WHERE estado = 'activo'")
        ).scalar()
        
        # Usar fecha seleccionada o fecha actual
        # Si no hay fecha, usar CURDATE() sin comillas
        if fecha:
            fecha_consulta = f"'{fecha}'"
        else:
            fecha_consulta = "CURDATE()"
        
        # Verificar si hay fichajes para la fecha seleccionada
        fichajes_existen = db.execute(
            text(f"""
                SELECT COUNT(*) FROM fichajes 
                WHERE fecha = {fecha_consulta}
            """)
        ).scalar()
        
        # Ausencias del día seleccionado (solo si hay fichajes para esa fecha)
        if fichajes_existen > 0:
            ausencias_hoy = db.execute(
                text(f"""
                    SELECT COUNT(*) FROM empleados e 
                    WHERE e.estado = 'activo' 
                    AND e.id NOT IN (
                        SELECT DISTINCT empleado_id FROM fichajes 
                        WHERE fecha = {fecha_consulta}
                    )
                """)
            ).scalar()
        else:
            # Si no hay fichajes para esa fecha, mostrar 0 ausencias
            ausencias_hoy = 0
        
        # Horas extras del mes actual (suma de todas las horas extras aprobadas)
        # Para demo: mostrar horas extras de los últimos 30 días
        horas_extras_mes = db.execute(
            text("""
                SELECT COALESCE(SUM(horas_extras), 0) 
                FROM horas_extras 
                WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                AND estado = 'aprobado'
            """)
        ).scalar()
        
        # Recibos pendientes (recibos generados o firmados)
        # Para demo: mostrar recibos pendientes de los últimos 3 meses
        recibos_pendientes = db.execute(
            text("""
                SELECT COUNT(*) FROM recibos_sueldo 
                WHERE estado IN ('generado', 'firmado')
                AND fecha_generacion >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
            """)
        ).scalar()
        
        return {
            "success": True,
            "data": {
                "empleados_activos": int(empleados_activos),
                "ausencias_hoy": int(ausencias_hoy),
                "horas_extras_mes": float(horas_extras_mes),
                "recibos_pendientes": int(recibos_pendientes)
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/api/dashboard/charts")
async def get_dashboard_charts(
    fecha: Optional[str] = Query(None, description="Fecha en formato YYYY-MM-DD"),
    db = Depends(get_db)
):
    """Obtener datos para charts del dashboard"""
    try:
        # Distribución por roles
        distribucion_roles = db.execute(
            text("""
                SELECT rol, COUNT(*) as cantidad 
                FROM empleados 
                WHERE estado = 'activo' 
                GROUP BY rol 
                ORDER BY cantidad DESC
            """)
        ).fetchall()
        
        # Usar fecha seleccionada o fecha actual
        # Si no hay fecha, usar CURDATE() sin comillas
        if fecha:
            fecha_consulta = f"'{fecha}'"
        else:
            fecha_consulta = "CURDATE()"
        
        # Asistencia semanal (datos reales de la semana que contiene la fecha seleccionada)
        # Obtener datos de asistencia para los últimos 7 días disponibles
        # Solo contar fichajes de entrada para evitar duplicados
        if fecha:
            # Si hay fecha específica, usar comillas
            asistencia_semanal = db.execute(
                text(f"""
                    SELECT 
                        DAYNAME(fecha) as dia,
                        COUNT(DISTINCT empleado_id) as asistencia
                    FROM fichajes 
                    WHERE fecha >= DATE_SUB('{fecha}', INTERVAL 6 DAY)
                    AND fecha <= '{fecha}'
                    AND tipo = 'entrada'
                    GROUP BY fecha, DAYNAME(fecha)
                    ORDER BY fecha
                """)
            ).fetchall()
        else:
            # Si no hay fecha, usar CURDATE() sin comillas
            asistencia_semanal = db.execute(
                text("""
                    SELECT 
                        DAYNAME(fecha) as dia,
                        COUNT(DISTINCT empleado_id) as asistencia
                    FROM fichajes 
                    WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL 6 DAY)
                    AND fecha <= CURDATE()
                    AND tipo = 'entrada'
                    GROUP BY fecha, DAYNAME(fecha)
                    ORDER BY fecha
                """)
            ).fetchall()
        
        # Convertir a formato esperado - SOLO datos reales
        asistencia_semanal = [{'dia': row.dia, 'asistencia': row.asistencia} for row in asistencia_semanal]
        
        # Horas extras por departamento (datos reales)
        # Como no hay departamento_id en empleados, usamos simulación por rol
        horas_extras_area = db.execute(
            text("""
                SELECT 
                    e.rol as area,
                    COALESCE(SUM(he.horas_extras), 0) as horas
                FROM empleados e
                LEFT JOIN horas_extras he ON e.id = he.empleado_id 
                    AND he.estado = 'aprobado'
                    AND MONTH(he.fecha) = MONTH(CURDATE())
                    AND YEAR(he.fecha) = YEAR(CURDATE())
                WHERE e.estado = 'activo'
                GROUP BY e.rol
                ORDER BY horas DESC
            """)
        ).fetchall()
        
        return {
            "success": True,
            "data": {
                "distribucion_roles": [
                    {"rol": row.rol, "cantidad": row.cantidad} 
                    for row in distribucion_roles
                ],
                "asistencia_semanal": asistencia_semanal,
                "horas_extras_area": [
                    {"area": row.area, "horas": float(row.horas)} 
                    for row in horas_extras_area
                ]
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# ============================================================================
# ENDPOINTS DE EMPLEADOS (P0 - Crítico)
# ============================================================================

@app.get("/api/empleados")
async def get_empleados(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    rol: Optional[str] = None,
    departamento: Optional[str] = None,
    estado: Optional[str] = None,
    db = Depends(get_db)
):
    """Obtener lista de empleados con paginación y filtros"""
    try:
        # Construir query base usando la tabla empleados
        query = text("""
            SELECT e.*, 'N/A' as departamento_nombre
            FROM empleados e
            WHERE 1=1
        """)
        
        params = {}
        
        # Aplicar filtros
        if search:
            query = text(str(query) + " AND (e.nombre LIKE :search OR e.apellido LIKE :search OR e.email LIKE :search)")
            params['search'] = f"%{search}%"
        
        if rol:
            query = text(str(query) + " AND e.rol = :rol")
            params['rol'] = rol
        
        if departamento:
            # Como no hay departamento_id, filtramos por rol que actúa como departamento
            query = text(str(query) + " AND e.rol = :departamento")
            params['departamento'] = departamento
        
        if estado:
            query = text(str(query) + " AND e.estado = :estado")
            params['estado'] = estado
        
        # Contar total
        count_query = text(str(query).replace("SELECT e.*, 'N/A' as departamento_nombre", "SELECT COUNT(*)"))
        total = db.execute(count_query, params).scalar()
        
        # Aplicar paginación
        offset = (page - 1) * size
        query = text(str(query) + " ORDER BY e.nombre, e.apellido LIMIT :size OFFSET :offset")
        params['size'] = size
        params['offset'] = offset
        
        empleados = db.execute(query, params).fetchall()
        
        return {
            "success": True,
            "data": {
                "empleados": [
                    {
                        "id": emp.id,
                        "nombre": emp.nombre,
                        "apellido": emp.apellido,
                        "email": emp.email,
                        "telefono": emp.telefono,
                        "rol": emp.rol,
                        "departamento": emp.rol,  # Usamos rol como departamento
                        "estado": emp.estado,
                        "fecha_ingreso": str(emp.fecha_ingreso) if emp.fecha_ingreso else None,
                        "horario_laboral": emp.horario_laboral
                    }
                    for emp in empleados
                ],
                "pagination": {
                    "page": page,
                    "size": size,
                    "total": total,
                    "pages": (total + size - 1) // size
                }
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/api/empleados/{empleado_id}")
async def get_empleado(empleado_id: int, db = Depends(get_db)):
    """Obtener detalle de un empleado"""
    try:
        empleado = db.execute(
            text("""
                SELECT e.*, d.nombre as departamento_nombre
                FROM empleados e
                LEFT JOIN departamentos d ON e.departamento_id = d.id
                WHERE e.id = :id
            """),
            {"id": empleado_id}
        ).fetchone()
        
        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")
        
        return {
            "success": True,
            "data": {
                "id": empleado.id,
                "nombre": empleado.nombre,
                "apellido": empleado.apellido,
                "email": empleado.email,
                "telefono": empleado.telefono,
                "domicilio": empleado.domicilio,
                "fecha_nacimiento": str(empleado.fecha_nacimiento),
                "nivel_estudio": empleado.nivel_estudio,
                "rol": empleado.rol,
                "departamento": empleado.departamento_nombre,
                "horario_laboral": empleado.horario_laboral,
                "estado": empleado.estado,
                "fecha_ingreso": str(empleado.fecha_ingreso)
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/api/empleados")
async def create_empleado(empleado_data: Dict[str, Any], db = Depends(get_db)):
    """Crear nuevo empleado"""
    try:
        # Validar datos requeridos
        required_fields = ["nombre", "apellido", "email", "rol"]
        for field in required_fields:
            if not empleado_data.get(field):
                raise HTTPException(status_code=400, detail=f"Campo {field} es requerido")
        
        # Insertar empleado
        result = db.execute(
            text("""
                INSERT INTO empleados (nombre, apellido, email, telefono, domicilio, 
                                     fecha_nacimiento, nivel_estudio, rol, horario_laboral, estado)
                VALUES (:nombre, :apellido, :email, :telefono, :domicilio, 
                       :fecha_nacimiento, :nivel_estudio, :rol, :horario_laboral, :estado)
            """),
            empleado_data
        )
        
        db.commit()
        
        return {
            "success": True,
            "data": {"id": result.lastrowid},
            "message": "Empleado creado exitosamente"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "error": str(e)
        }

@app.put("/api/empleados/{empleado_id}")
async def update_empleado(empleado_id: int, empleado_data: Dict[str, Any], db = Depends(get_db)):
    """Actualizar empleado"""
    try:
        # Verificar que existe
        empleado = db.execute(
            text("SELECT id FROM empleados WHERE id = :id"),
            {"id": empleado_id}
        ).fetchone()
        
        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")
        
        # Actualizar
        db.execute(
            text("""
                UPDATE empleados 
                SET nombre = :nombre, apellido = :apellido, email = :email,
                    telefono = :telefono, domicilio = :domicilio, rol = :rol,
                    horario_laboral = :horario_laboral, estado = :estado
                WHERE id = :id
            """),
            {**empleado_data, "id": empleado_id}
        )
        
        db.commit()
        
        return {
            "success": True,
            "message": "Empleado actualizado exitosamente"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "error": str(e)
        }

@app.delete("/api/empleados/{empleado_id}")
async def delete_empleado(empleado_id: int, db = Depends(get_db)):
    """Eliminar empleado (baja lógica)"""
    try:
        # Verificar que existe
        empleado = db.execute(
            text("SELECT id FROM empleados WHERE id = :id"),
            {"id": empleado_id}
        ).fetchone()
        
        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")
        
        # Baja lógica
        db.execute(
            text("UPDATE empleados SET estado = 'inactivo' WHERE id = :id"),
            {"id": empleado_id}
        )
        
        db.commit()
        
        return {
            "success": True,
            "message": "Empleado dado de baja exitosamente"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/api/stats")
async def get_stats(db = Depends(get_db)):
    """Obtener estadísticas generales"""
    try:
        # Empleados activos
        empleados_activos = db.execute(
            text("SELECT COUNT(*) FROM empleados WHERE estado = 'activo'")
        ).scalar()
        
        # Total empleados
        total_empleados = db.execute(
            text("SELECT COUNT(*) FROM empleados")
        ).scalar()
        
        # Fichajes hoy
        fichajes_hoy = db.execute(
            text("SELECT COUNT(*) FROM fichajes WHERE fecha = CURDATE()")
        ).scalar()
        
        # Recibos pendientes
        recibos_pendientes = db.execute(
            text("SELECT COUNT(*) FROM recibos_sueldo WHERE estado IN ('generado', 'firmado')")
        ).scalar()
        
        return {
            "success": True,
            "data": {
                "empleados_activos": empleados_activos,
                "total_empleados": total_empleados,
                "fichajes_hoy": fichajes_hoy,
                "recibos_pendientes": recibos_pendientes
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/api/empleados/export")
async def export_empleados_csv(
    search: Optional[str] = None,
    rol: Optional[str] = None,
    estado: Optional[str] = None,
    db = Depends(get_db)
):
    """Exportar empleados a CSV"""
    try:
        # Construir query
        query = text("""
            SELECT e.nombre, e.apellido, e.email, e.telefono, e.rol, e.estado, e.fecha_ingreso
            FROM empleados e
            WHERE 1=1
        """)
        
        params = {}
        
        if search:
            query = text(str(query) + " AND (e.nombre LIKE :search OR e.apellido LIKE :search)")
            params['search'] = f"%{search}%"
        
        if rol:
            query = text(str(query) + " AND e.rol = :rol")
            params['rol'] = rol
        
        if estado:
            query = text(str(query) + " AND e.estado = :estado")
            params['estado'] = estado
        
        empleados = db.execute(query, params).fetchall()
        
        # Crear CSV
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Nombre', 'Apellido', 'Email', 'Teléfono', 'Rol', 'Estado', 'Fecha Ingreso'])
        
        for emp in empleados:
            writer.writerow([
                emp.nombre, emp.apellido, emp.email, emp.telefono,
                emp.rol, emp.estado, str(emp.fecha_ingreso) if emp.fecha_ingreso else ''
            ])
        
        output.seek(0)
        
        return JSONResponse(
            content={"success": True, "data": output.getvalue()},
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=empleados.csv"}
        )
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# ============================================================================
# ENDPOINTS DE FICHAJES (P0 - Crítico)
# ============================================================================

@app.get("/api/fichajes")
async def get_fichajes(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    fecha: Optional[str] = None,
    empleado_id: Optional[int] = None,
    departamento_id: Optional[int] = None,
    db = Depends(get_db)
):
    """Obtener lista de fichajes con filtros"""
    try:
        # Construir query base usando la tabla fichajes
        query = text("""
            SELECT 
                f.id, f.empleado_id, f.fecha, f.hora_entrada, f.hora_salida, 
                f.horas_trabajadas, f.tipo, f.ubicacion, f.dispositivo, f.observaciones,
                e.nombre, e.apellido, e.rol, e.rol as departamento
            FROM fichajes f
            JOIN empleados e ON f.empleado_id = e.id
            WHERE 1=1
        """)
        
        params = {}
        
        if fecha:
            query = text(str(query) + " AND f.fecha = :fecha")
            params['fecha'] = fecha
        
        if empleado_id:
            query = text(str(query) + " AND f.empleado_id = :empleado_id")
            params['empleado_id'] = empleado_id
        
        if departamento_id:
            query = text(str(query) + " AND e.departamento_id = :departamento_id")
            params['departamento_id'] = departamento_id
        
        # Contar total
        count_query = text(str(query).replace("SELECT f.id, f.empleado_id, f.fecha, f.hora_entrada, f.hora_salida, f.horas_trabajadas, f.tipo, f.ubicacion, f.dispositivo, f.observaciones, e.nombre, e.apellido, e.rol, e.rol as departamento", "SELECT COUNT(*)"))
        total = db.execute(count_query, params).scalar()
        
        # Aplicar paginación
        offset = (page - 1) * size
        query = text(str(query) + " ORDER BY f.fecha DESC, f.hora_entrada DESC LIMIT :size OFFSET :offset")
        params['size'] = size
        params['offset'] = offset
        
        fichajes = db.execute(query, params).fetchall()
        
        return {
            "success": True,
            "data": {
                "fichajes": [
                    {
                        "id": f.id,
                        "empleado": f"{f.nombre} {f.apellido}",
                        "rol": f.rol,
                        "departamento": f.departamento,
                        "fecha": str(f.fecha),
                        "hora_entrada": str(f.hora_entrada) if f.hora_entrada else None,
                        "hora_salida": str(f.hora_salida) if f.hora_salida else None,
                        "horas_trabajadas": float(f.horas_trabajadas) if f.horas_trabajadas else 0,
                        "tipo": f.tipo,
                        "ubicacion": f.ubicacion,
                        "dispositivo": f.dispositivo,
                        "observaciones": f.observaciones
                    }
                    for f in fichajes
                ],
                "pagination": {
                    "page": page,
                    "size": size,
                    "total": total,
                    "pages": (total + size - 1) // size
                }
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.patch("/api/fichajes/{fichaje_id}")
async def ajustar_fichaje(fichaje_id: int, ajuste_data: Dict[str, Any], db = Depends(get_db)):
    """Ajustar fichaje manualmente"""
    try:
        # Verificar que existe
        fichaje = db.execute(
            text("SELECT id FROM fichajes WHERE id = :id"),
            {"id": fichaje_id}
        ).fetchone()
        
        if not fichaje:
            raise HTTPException(status_code=404, detail="Fichaje no encontrado")
        
        # Actualizar fichaje
        db.execute(
            text("""
                UPDATE fichajes 
                SET hora_entrada = :hora_entrada, hora_salida = :hora_salida,
                    horas_trabajadas = :horas_trabajadas, estado = :estado,
                    motivo_ajuste = :motivo_ajuste, ajustado_por = :ajustado_por
                WHERE id = :id
            """),
            {**ajuste_data, "id": fichaje_id}
        )
        
        db.commit()
        
        return {
            "success": True,
            "message": "Fichaje ajustado exitosamente"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/api/fichajes/export")
async def export_fichajes_csv(
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    empleado_id: Optional[int] = None,
    db = Depends(get_db)
):
    """Exportar fichajes a CSV"""
    try:
        # Construir query
        query = text("""
            SELECT e.nombre, e.apellido, e.rol, f.fecha, f.hora_entrada, 
                   f.hora_salida, f.horas_trabajadas, f.estado
            FROM fichajes f
            JOIN empleados e ON f.empleado_id = e.id
            WHERE 1=1
        """)
        
        params = {}
        
        if fecha_inicio:
            query = text(str(query) + " AND f.fecha >= :fecha_inicio")
            params['fecha_inicio'] = fecha_inicio
        
        if fecha_fin:
            query = text(str(query) + " AND f.fecha <= :fecha_fin")
            params['fecha_fin'] = fecha_fin
        
        if empleado_id:
            query = text(str(query) + " AND f.empleado_id = :empleado_id")
            params['empleado_id'] = empleado_id
        
        fichajes = db.execute(query, params).fetchall()
        
        # Crear CSV
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Empleado', 'Rol', 'Fecha', 'Entrada', 'Salida', 'Horas', 'Estado'])
        
        for f in fichajes:
            writer.writerow([
                f"{f.nombre} {f.apellido}", f.rol, str(f.fecha),
                str(f.hora_entrada), str(f.hora_salida) if f.hora_salida else '',
                f.horas_trabajadas, f.estado
            ])
        
        output.seek(0)
        
        return JSONResponse(
            content={"success": True, "data": output.getvalue()},
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=fichajes.csv"}
        )
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# ============================================================================
# ENDPOINTS DE RECIBOS (P0 - Crítico)
# ============================================================================

@app.get("/api/recibos")
async def get_recibos(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    periodo: Optional[str] = None,
    estado: Optional[str] = None,
    empleado_id: Optional[int] = None,
    db = Depends(get_db)
):
    """Obtener lista de recibos con filtros"""
    try:
        # Construir query base adaptada a tu estructura
        query = text("""
            SELECT 
                r.id, r.empleado_id, r.mes, r.año, r.sueldo_base, r.horas_extras,
                r.bonificaciones, r.descuentos, r.sueldo_neto, r.estado,
                r.fecha_generacion, r.fecha_firma_empleado, r.fecha_aprobacion_supervisor,
                r.observaciones,
                e.nombre, e.apellido, e.rol
            FROM recibos_sueldo r
            JOIN empleados e ON r.empleado_id = e.id
            WHERE 1=1
        """)
        
        params = {}
        
        if periodo:
            # Convertir periodo YYYY-MM a mes y año
            try:
                año, mes = periodo.split('-')
                query = text(str(query) + " AND r.año = :año AND r.mes = :mes")
                params['año'] = int(año)
                params['mes'] = int(mes)
            except:
                pass
        
        if estado:
            query = text(str(query) + " AND r.estado = :estado")
            params['estado'] = estado
        
        if empleado_id:
            query = text(str(query) + " AND r.empleado_id = :empleado_id")
            params['empleado_id'] = empleado_id
        
        # Contar total
        count_query = text(str(query).replace("SELECT r.id, r.empleado_id, r.mes, r.año, r.sueldo_base, r.horas_extras, r.bonificaciones, r.descuentos, r.sueldo_neto, r.estado, r.fecha_generacion, r.fecha_firma_empleado, r.fecha_aprobacion_supervisor, r.observaciones, e.nombre, e.apellido, e.rol", "SELECT COUNT(*)"))
        total = db.execute(count_query, params).scalar()
        
        # Aplicar paginación
        offset = (page - 1) * size
        query = text(str(query) + " ORDER BY r.año DESC, r.mes DESC, r.fecha_generacion DESC LIMIT :size OFFSET :offset")
        params['size'] = size
        params['offset'] = offset
        
        recibos = db.execute(query, params).fetchall()
        
        return {
            "success": True,
            "data": {
                "recibos": [
                    {
                        "id": r.id,
                        "empleado": f"{r.nombre} {r.apellido}",
                        "rol": r.rol,
                        "periodo": f"{r.año}-{r.mes:02d}",
                        "sueldo_base": float(r.sueldo_base),
                        "horas_extras": float(r.horas_extras) if r.horas_extras else 0,
                        "bonificaciones": float(r.bonificaciones) if r.bonificaciones else 0,
                        "descuentos": float(r.descuentos) if r.descuentos else 0,
                        "sueldo_neto": float(r.sueldo_neto),
                        "estado": r.estado,
                        "fecha_generacion": str(r.fecha_generacion) if r.fecha_generacion else None,
                        "fecha_firma": str(r.fecha_firma_empleado) if r.fecha_firma_empleado else None,
                        "fecha_aprobacion": str(r.fecha_aprobacion_supervisor) if r.fecha_aprobacion_supervisor else None,
                        "observaciones": r.observaciones
                    }
                    for r in recibos
                ],
                "pagination": {
                    "page": page,
                    "size": size,
                    "total": total,
                    "pages": (total + size - 1) // size
                }
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/api/recibos/generar")
async def generar_recibo(recibo_data: Dict[str, Any], db = Depends(get_db)):
    """Generar recibo de sueldo"""
    try:
        # Validar datos
        if not recibo_data.get("empleado_id") or not recibo_data.get("periodo"):
            raise HTTPException(status_code=400, detail="empleado_id y periodo son requeridos")
        
        # Generar recibo
        result = db.execute(
            text("""
                INSERT INTO recibos_sueldo (empleado_id, periodo, sueldo_base, horas_extras, sueldo_neto, estado)
                VALUES (:empleado_id, :periodo, :sueldo_base, :horas_extras, :sueldo_neto, 'generado')
            """),
            recibo_data
        )
        
        db.commit()
        
        return {
            "success": True,
            "data": {"id": result.lastrowid},
            "message": "Recibo generado exitosamente"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/api/recibos/{recibo_id}/firmar")
async def firmar_recibo(recibo_id: int, db = Depends(get_db)):
    """Firmar recibo (empleado)"""
    try:
        db.execute(
            text("UPDATE recibos_sueldo SET estado = 'firmado' WHERE id = :id"),
            {"id": recibo_id}
        )
        db.commit()
        
        return {
            "success": True,
            "message": "Recibo firmado exitosamente"
        }
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/api/recibos/{recibo_id}/aprobar")
async def aprobar_recibo(recibo_id: int, db = Depends(get_db)):
    """Aprobar recibo (supervisor/RRHH)"""
    try:
        db.execute(
            text("UPDATE recibos_sueldo SET estado = 'aprobado' WHERE id = :id"),
            {"id": recibo_id}
        )
        db.commit()
        
        return {
            "success": True,
            "message": "Recibo aprobado exitosamente"
        }
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/api/recibos/{recibo_id}/publicar")
async def publicar_recibo(recibo_id: int, db = Depends(get_db)):
    """Publicar recibo"""
    try:
        db.execute(
            text("UPDATE recibos_sueldo SET estado = 'publicado' WHERE id = :id"),
            {"id": recibo_id}
        )
        db.commit()
        
        return {
            "success": True,
            "message": "Recibo publicado exitosamente"
        }
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/api/recibos/{recibo_id}/descargar")
async def descargar_recibo(recibo_id: int, db = Depends(get_db)):
    """Descargar recibo en PDF"""
    try:
        recibo = db.execute(
            text("""
                SELECT r.*, e.nombre, e.apellido, e.rol
                FROM recibos_sueldo r
                JOIN empleados e ON r.empleado_id = e.id
                WHERE r.id = :id
            """),
            {"id": recibo_id}
        ).fetchone()
        
        if not recibo:
            raise HTTPException(status_code=404, detail="Recibo no encontrado")
        
        # Por ahora retornamos JSON, en el futuro será PDF
        return {
            "success": True,
            "data": {
                "id": recibo.id,
                "empleado": f"{recibo.nombre} {recibo.apellido}",
                "rol": recibo.rol,
                "periodo": recibo.periodo,
                "sueldo_base": recibo.sueldo_base,
                "horas_extras": recibo.horas_extras,
                "sueldo_neto": recibo.sueldo_neto,
                "estado": recibo.estado
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# ============================================================================
# ENDPOINTS DE UTILIDAD
# ============================================================================

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "Chango_ADM API - Sistema de Gestión RRHH",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check del sistema"""
    try:
        # Verificar conexión a BD
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/test-db")
async def test_database(db = Depends(get_db)):
    """Test de conexión a base de datos"""
    try:
        # Contar empleados
        empleados_count = db.execute(text("SELECT COUNT(*) FROM empleados")).scalar()
        
        # Obtener muestra de empleados
        empleados_muestra = db.execute(
            text("SELECT id, nombre, apellido, rol, horario_laboral, estado FROM empleados LIMIT 5")
        ).fetchall()
        
        # Contar fichajes
        fichajes_count = db.execute(text("SELECT COUNT(*) FROM fichajes")).scalar()
        
        # Contar recibos
        recibos_count = db.execute(text("SELECT COUNT(*) FROM recibos_sueldo")).scalar()
        
        # Contar usuarios
        usuarios_count = db.execute(text("SELECT COUNT(*) FROM usuarios")).scalar()
        
        return {
            "status": "success",
            "message": "Datos reales de la base de datos actual",
            "total_empleados": empleados_count,
            "total_fichajes": fichajes_count,
            "total_recibos": recibos_count,
            "total_usuarios": usuarios_count,
            "muestra_empleados": [
                {
                    "id": emp.id,
                    "nombre": emp.nombre,
                    "apellido": emp.apellido,
                    "rol": emp.rol,
                    "horario_laboral": emp.horario_laboral,
                    "estado": emp.estado
                }
                for emp in empleados_muestra
            ],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/api/dashboard/fechas-disponibles")
async def get_fechas_disponibles(db = Depends(get_db)):
    """Obtener fechas disponibles en la base de datos"""
    try:
        # Fechas de fichajes disponibles
        fechas_fichajes = db.execute(
            text("SELECT DISTINCT fecha FROM fichajes ORDER BY fecha DESC LIMIT 30")
        ).fetchall()
        
        # Fechas de recibos disponibles
        fechas_recibos = db.execute(
            text("SELECT DISTINCT fecha_generacion FROM recibos_sueldo ORDER BY fecha_generacion DESC LIMIT 30")
        ).fetchall()
        
        return {
            "success": True,
            "data": {
                "fechas_fichajes": [str(f.fecha) for f in fechas_fichajes],
                "fechas_recibos": [str(f.fecha_generacion) for f in fechas_recibos if f.fecha_generacion]
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/api/debug/tablas")
async def debug_tablas(
    fecha: Optional[str] = Query(None, description="Fecha en formato YYYY-MM-DD"),
    db = Depends(get_db)
):
    """Debug de datos de las tablas para verificar información"""
    try:
        # Si no hay fecha, usar CURDATE() sin comillas
        if fecha:
            fecha_consulta = f"'{fecha}'"
        else:
            fecha_consulta = "CURDATE()"
        
        # Datos de empleados
        empleados = db.execute(
            text("SELECT id, nombre, apellido, rol, estado FROM empleados LIMIT 10")
        ).fetchall()
        
        # Fichajes de la fecha seleccionada
        fichajes_fecha = db.execute(
            text(f"""
                SELECT f.id, f.empleado_id, e.nombre, e.apellido, f.fecha, 
                       f.hora_entrada, f.hora_salida, f.horas_trabajadas
                FROM fichajes f
                JOIN empleados e ON f.empleado_id = e.id
                WHERE f.fecha = {fecha_consulta}
                LIMIT 10
            """)
        ).fetchall()
        
        # Total de fichajes por fecha
        total_fichajes_fecha = db.execute(
            text(f"SELECT COUNT(*) FROM fichajes WHERE fecha = {fecha_consulta}")
        ).scalar()
        
        # Empleados activos
        empleados_activos = db.execute(
            text("SELECT COUNT(*) FROM empleados WHERE estado = 'activo'")
        ).scalar()
        
        # Horas extras
        horas_extras = db.execute(
            text(f"""
                SELECT he.id, he.empleado_id, e.nombre, e.apellido, he.fecha, 
                       he.horas_extras, he.estado
                FROM horas_extras he
                JOIN empleados e ON he.empleado_id = e.id
                WHERE he.fecha >= DATE_SUB({fecha_consulta}, INTERVAL 30 DAY)
                LIMIT 10
            """)
        ).fetchall()
        
        # Recibos de sueldo
        recibos = db.execute(
            text(f"""
                SELECT rs.id, rs.empleado_id, e.nombre, e.apellido, rs.fecha_generacion, 
                       rs.estado, rs.sueldo_base, rs.sueldo_neto
                FROM recibos_sueldo rs
                JOIN empleados e ON rs.empleado_id = e.id
                WHERE rs.fecha_generacion >= DATE_SUB({fecha_consulta}, INTERVAL 90 DAY)
                LIMIT 10
            """)
        ).fetchall()
        
        # Fechas disponibles en fichajes
        fechas_disponibles = db.execute(
            text("SELECT DISTINCT fecha FROM fichajes ORDER BY fecha DESC LIMIT 10")
        ).fetchall()
        
        return {
            "success": True,
            "data": {
                "fecha_consulta": fecha_consulta,
                "empleados": {
                    "total_activos": empleados_activos,
                    "muestra": [
                        {
                            "id": e.id,
                            "nombre": e.nombre,
                            "apellido": e.apellido,
                            "rol": e.rol,
                            "estado": e.estado
                        } for e in empleados
                    ]
                },
                "fichajes": {
                    "total_fecha": total_fichajes_fecha,
                    "muestra": [
                        {
                            "id": f.id,
                            "empleado_id": f.empleado_id,
                            "nombre": f.nombre,
                            "apellido": f.apellido,
                            "fecha": str(f.fecha),
                            "hora_entrada": str(f.hora_entrada) if f.hora_entrada else None,
                            "hora_salida": str(f.hora_salida) if f.hora_salida else None,
                            "horas_trabajadas": float(f.horas_trabajadas) if f.horas_trabajadas else 0
                        } for f in fichajes_fecha
                    ]
                },
                "horas_extras": {
                    "muestra": [
                        {
                            "id": he.id,
                            "empleado_id": he.empleado_id,
                            "nombre": he.nombre,
                            "apellido": he.apellido,
                            "fecha": str(he.fecha),
                            "horas_extras": float(he.horas_extras) if he.horas_extras else 0,
                            "estado": he.estado
                        } for he in horas_extras
                    ]
                },
                "recibos": {
                    "muestra": [
                        {
                            "id": rs.id,
                            "empleado_id": rs.empleado_id,
                            "nombre": rs.nombre,
                            "apellido": rs.apellido,
                            "fecha_generacion": str(rs.fecha_generacion) if rs.fecha_generacion else None,
                            "estado": rs.estado,
                            "sueldo_base": float(rs.sueldo_base) if rs.sueldo_base else 0,
                            "sueldo_neto": float(rs.sueldo_neto) if rs.sueldo_neto else 0
                        } for rs in recibos
                    ]
                },
                "fechas_disponibles": [str(f.fecha) for f in fechas_disponibles]
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/debug-kpis")
async def debug_kpis(db = Depends(get_db)):
    """Debug de KPIs para entender los datos"""
    try:
        # Empleados activos
        empleados_activos = db.execute(text("SELECT COUNT(*) FROM empleados WHERE estado = 'activo'")).scalar()
        total_empleados = db.execute(text("SELECT COUNT(*) FROM empleados")).scalar()
        
        # Fichajes de hoy
        fichajes_hoy = db.execute(text("SELECT COUNT(*) FROM fichajes WHERE fecha = CURDATE()")).scalar()
        
        # Fechas de fichajes disponibles
        fechas_fichajes = db.execute(text("SELECT DISTINCT fecha FROM fichajes ORDER BY fecha DESC LIMIT 5")).fetchall()
        
        # Horas extras del mes
        horas_extras_mes = db.execute(text("""
            SELECT COALESCE(SUM(horas_extras), 0) 
            FROM horas_extras 
            WHERE MONTH(fecha) = MONTH(CURDATE()) 
            AND YEAR(fecha) = YEAR(CURDATE())
            AND estado = 'aprobado'
        """)).scalar()
        
        # Recibos del mes actual
        recibos_mes_actual = db.execute(text("""
            SELECT COUNT(*) FROM recibos_sueldo 
            WHERE mes = MONTH(CURDATE()) 
            AND año = YEAR(CURDATE())
        """)).scalar()
        
        # Recibos pendientes
        recibos_pendientes = db.execute(text("""
            SELECT COUNT(*) FROM recibos_sueldo 
            WHERE estado IN ('generado', 'firmado')
        """)).scalar()
        
        # Estados de recibos
        estados_recibos = db.execute(text("""
            SELECT estado, COUNT(*) as cantidad 
            FROM recibos_sueldo 
            GROUP BY estado
        """)).fetchall()
        
        return {
            "status": "success",
            "debug_info": {
                "empleados": {
                    "total": total_empleados,
                    "activos": empleados_activos,
                    "inactivos": total_empleados - empleados_activos
                },
                "fichajes": {
                    "hoy": fichajes_hoy,
                    "fechas_disponibles": [str(f.fecha) for f in fechas_fichajes]
                },
                "horas_extras": {
                    "mes_actual": float(horas_extras_mes)
                },
                "recibos": {
                    "mes_actual": recibos_mes_actual,
                    "pendientes": recibos_pendientes,
                    "estados": [{"estado": r.estado, "cantidad": r.cantidad} for r in estados_recibos]
                },
                "fecha_actual": datetime.now().strftime("%Y-%m-%d")
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.get("/api/debug/asistencia-semanal")
async def debug_asistencia_semanal(
    fecha: Optional[str] = Query(None, description="Fecha en formato YYYY-MM-DD"),
    db = Depends(get_db)
):
    """Debug específico para asistencia semanal"""
    try:
        # Si no hay fecha, usar CURDATE() sin comillas
        if fecha:
            fecha_consulta = f"'{fecha}'"
        else:
            fecha_consulta = "CURDATE()"
        
        # Consulta original
        asistencia_original = db.execute(
            text(f"""
                SELECT 
                    fecha,
                    DAYNAME(fecha) as dia,
                    COUNT(DISTINCT empleado_id) as asistencia
                FROM fichajes 
                WHERE fecha >= DATE_SUB('{fecha_consulta}', INTERVAL 6 DAY)
                AND fecha <= '{fecha_consulta}'
                GROUP BY fecha, DAYNAME(fecha)
                ORDER BY fecha
            """)
        ).fetchall()
        
        # Consulta con filtro de entrada
        asistencia_entrada = db.execute(
            text(f"""
                SELECT 
                    fecha,
                    DAYNAME(fecha) as dia,
                    COUNT(DISTINCT empleado_id) as asistencia
                FROM fichajes 
                WHERE fecha >= DATE_SUB('{fecha_consulta}', INTERVAL 6 DAY)
                AND fecha <= '{fecha_consulta}'
                AND tipo = 'entrada'
                GROUP BY fecha, DAYNAME(fecha)
                ORDER BY fecha
            """)
        ).fetchall()
        
        # Total de fichajes por tipo en el rango
        total_por_tipo = db.execute(
            text(f"""
                SELECT 
                    tipo,
                    COUNT(*) as total
                FROM fichajes 
                WHERE fecha >= DATE_SUB('{fecha_consulta}', INTERVAL 6 DAY)
                AND fecha <= '{fecha_consulta}'
                GROUP BY tipo
            """)
        ).fetchall()
        
        return {
            "success": True,
            "data": {
                "fecha_consulta": fecha_consulta,
                "rango_busqueda": f"Desde {fecha_consulta} - 6 días hasta {fecha_consulta}",
                "asistencia_original": [
                    {
                        "fecha": str(row.fecha),
                        "dia": row.dia,
                        "asistencia": row.asistencia
                    } for row in asistencia_original
                ],
                "asistencia_entrada": [
                    {
                        "fecha": str(row.fecha),
                        "dia": row.dia,
                        "asistencia": row.asistencia
                    } for row in asistencia_entrada
                ],
                "total_por_tipo": [
                    {
                        "tipo": row.tipo,
                        "total": row.total
                    } for row in total_por_tipo
                ]
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.RELOAD
    )