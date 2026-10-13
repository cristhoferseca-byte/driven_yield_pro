# app/routers/mecanicos.py
import datetime as dt
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel

from app.database import get_db
from app.security import require_admin, get_current_user

router = APIRouter(prefix="/api/mecanicos", tags=["mecanicos"])


# ── Schemas ───────────────────────────────────────────────────────────────────

class MecanicoBody(BaseModel):
    nombre:       str
    especialidad: Optional[str] = None
    telefono:     Optional[str] = None
    disponible:   Optional[bool] = True


# ── Helpers ───────────────────────────────────────────────────────────────────

def _fmt_decimal(val) -> float:
    """Convierte objetos Decimal de base de datos a float para respuesta JSON."""
    return float(val) if isinstance(val, Decimal) else (val or 0.0)

def _fmt_hora(value) -> str:
    """Convierte timedelta a formato de cadena HH:MM."""
    if value is None:
        return ""
    if isinstance(value, dt.timedelta):
        total = int(value.total_seconds())
        h, rem = divmod(total, 3600)
        m, _   = divmod(rem, 60)
        return f"{h:02d}:{m:02d}"
    return str(value)

def _fmt_cita(row: dict) -> dict:
    """Formatea la fecha, hora y monto de una cita asignada a un mecánico."""
    if row.get("fecha"):
        row["fecha"] = str(row["fecha"])
    if "hora" in row:
        row["hora"] = _fmt_hora(row["hora"])
    if "monto" in row:
        row["monto"] = _fmt_decimal(row["monto"])
    return row


# ── GET /api/mecanicos ────────────────────────────────────────────────────────

@router.get("")
def get_mecanicos():
    """Retorna el listado completo de mecánicos activos junto con sus métricas de citas."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT
                m.id_mecanico   AS id,
                m.nombre,
                m.especialidad,
                m.telefono,
                m.disponible,
                COUNT(c.id_cita)                                        AS total_citas,
                COALESCE(SUM(CASE WHEN c.estado = 'completada' THEN 1 ELSE 0 END), 0) AS citas_completadas,
                COALESCE(SUM(CASE WHEN c.estado = 'pendiente' THEN 1 ELSE 0 END), 0)  AS citas_pendientes,
                COALESCE(SUM(CASE WHEN c.estado = 'completada'
                                  THEN c.monto ELSE 0 END), 0)         AS total_generado
            FROM mecanico m
            LEFT JOIN cita c ON c.id_mecanico = m.id_mecanico
            WHERE m.activo = 1
            GROUP BY m.id_mecanico
            ORDER BY m.nombre
        """)
        rows = cur.fetchall()

    for r in rows:
        r["total_generado"] = _fmt_decimal(r["total_generado"])
        r["disponible"]     = bool(r["disponible"])
    return {"total": len(rows), "mecanicos": rows}


# ── GET /api/mecanicos/ranking ────────────────────────────────────────────────

@router.get("/ranking")
def get_ranking(authorization: str = Header(None)):
    """Obtiene el ranking de rendimiento de mecánicos ordenado por total generado."""
    get_current_user(authorization)

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT
                m.id_mecanico                                            AS id,
                m.nombre,
                m.especialidad,
                m.disponible,
                COUNT(c.id_cita)                                         AS total_citas,
                COALESCE(SUM(CASE WHEN c.estado = 'completada' THEN 1 ELSE 0 END), 0) AS citas_completadas,
                COALESCE(SUM(CASE WHEN c.estado = 'completada'
                                  THEN c.monto ELSE 0 END), 0)          AS total_generado,
                COALESCE(AVG(CASE WHEN c.estado = 'completada'
                                  THEN c.monto END), 0)                 AS promedio_por_cita
            FROM mecanico m
            LEFT JOIN cita c ON c.id_mecanico = m.id_mecanico
            WHERE m.activo = 1
            GROUP BY m.id_mecanico
            ORDER BY total_generado DESC
        """)
        rows = cur.fetchall()

    ranking = []
    for i, r in enumerate(rows, start=1):
        ranking.append({
            "posicion":          i,
            "id":                r["id"],
            "nombre":            r["nombre"],
            "especialidad":      r.get("especialidad"),
            "disponible":        bool(r["disponible"]),
            "total_citas":       r["total_citas"],
            "citas_completadas": r["citas_completadas"],
            "total_generado":    _fmt_decimal(r["total_generado"]),
            "promedio_por_cita": _fmt_decimal(r["promedio_por_cita"]),
        })

    return {
        "titulo":  "🏆 Ranking de mecánicos por ingresos generados",
        "ranking": ranking
    }


# ── GET /api/mecanicos/{id} ───────────────────────────────────────────────────

@router.get("/{mecanico_id}")
def get_mecanico(mecanico_id: int):
    """Obtiene el detalle individual de un mecánico por su identificador."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id_mecanico AS id, nombre, especialidad, telefono, disponible
            FROM mecanico WHERE id_mecanico = %s AND activo = 1
        """, (mecanico_id,))
        row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Mecánico no encontrado")
    row["disponible"] = bool(row["disponible"])
    return row


# ── GET /api/mecanicos/{id}/ingresos ─────────────────────────────────────────

@router.get("/{mecanico_id}/ingresos")
def get_ingresos(mecanico_id: int, authorization: str = Header(None)):
    """Obtiene el historial detallado de citas e ingresos asociados a un mecánico."""
    get_current_user(authorization)

    with get_db() as conn:
        cur = conn.cursor()

        cur.execute("""
            SELECT id_mecanico AS id, nombre, especialidad, disponible
            FROM mecanico WHERE id_mecanico = %s AND activo = 1
        """, (mecanico_id,))
        mec = cur.fetchone()
        if not mec:
            raise HTTPException(status_code=404, detail="Mecánico no encontrado")

        cur.execute("""
            SELECT
                COUNT(*)                                                   AS total_citas,
                COALESCE(SUM(CASE WHEN estado = 'completada' THEN 1 ELSE 0 END), 0) AS completadas,
                COALESCE(SUM(CASE WHEN estado = 'pendiente' THEN 1 ELSE 0 END), 0)  AS pendientes,
                COALESCE(SUM(CASE WHEN estado = 'cancelada' THEN 1 ELSE 0 END), 0)  AS canceladas,
                COALESCE(SUM(CASE WHEN estado='completada'
                                  THEN monto ELSE 0 END), 0)             AS total_generado,
                COALESCE(AVG(CASE WHEN estado='completada'
                                  THEN monto END), 0)                    AS promedio_cita
            FROM cita WHERE id_mecanico = %s
        """, (mecanico_id,))
        resumen = cur.fetchone()

        cur.execute("""
            SELECT
                c.id_cita                       AS id,
                u.nombre                         AS cliente,
                CONCAT(v.marca, ' ', v.modelo)  AS vehiculo,
                v.numero_de_placa               AS placa,
                s.nombre                         AS servicio,
                c.fecha,
                c.hora,
                c.monto,
                c.estado
            FROM cita c
            LEFT JOIN usuario  u ON c.id_usuario  = u.id_usuario
            LEFT JOIN vehiculo v ON c.id_vehiculo = v.id_vehiculo
            LEFT JOIN servicio s ON c.id_servicio = s.id_servicio
            WHERE c.id_mecanico = %s
            ORDER BY c.fecha DESC, c.hora DESC
        """, (mecanico_id,))
        citas = cur.fetchall()

    return {
        "mecanico": {
            "id":           mec["id"],
            "nombre":       mec["nombre"],
            "especialidad": mec.get("especialidad"),
            "disponible":   bool(mec["disponible"]),
        },
        "resumen": {
            "total_citas":    resumen["total_citas"],
            "completadas":    resumen["completadas"],
            "pendientes":     resumen["pendientes"],
            "canceladas":     resumen["canceladas"],
            "total_generado": _fmt_decimal(resumen["total_generado"]),
            "promedio_cita":  _fmt_decimal(resumen["promedio_cita"]),
        },
        "citas": [_fmt_cita(c) for c in citas]
    }


# ── POST /api/mecanicos ───────────────────────────────────────────────────────

@router.post("")
def crear_mecanico(body: MecanicoBody, authorization: str = Header(None)):
    """Crea un nuevo registro de mecánico en el sistema (requiere rol admin)."""
    require_admin(authorization)

    if not body.nombre.strip():
        raise HTTPException(status_code=400, detail="El nombre es obligatorio")

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO mecanico (nombre, especialidad, telefono, disponible)
            VALUES (%s, %s, %s, %s) RETURNING id_mecanico
        """, (
            body.nombre.strip(),
            body.especialidad,
            body.telefono,
            1 if body.disponible else 0,
        ))
        new_id = cur.fetchone()["id_mecanico"]

    return {
        "ok":      True,
        "mensaje": "Mecánico creado correctamente ✅",
        "mecanico": {
            "id":          new_id,
            "nombre":      body.nombre.strip(),
            "especialidad":body.especialidad,
            "telefono":    body.telefono,
            "disponible":  body.disponible,
        }
    }


# ── PUT /api/mecanicos/{id} ───────────────────────────────────────────────────

@router.put("/{mecanico_id}")
def actualizar_mecanico(mecanico_id: int, body: MecanicoBody, authorization: str = Header(None)):
    """Actualiza los datos de un mecánico existente (requiere rol admin)."""
    require_admin(authorization)

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id_mecanico FROM mecanico WHERE id_mecanico = %s AND activo = 1", (mecanico_id,))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Mecánico no encontrado")

        cur.execute("""
            UPDATE mecanico
            SET nombre = %s, especialidad = %s, telefono = %s, disponible = %s
            WHERE id_mecanico = %s
        """, (
            body.nombre.strip(),
            body.especialidad,
            body.telefono,
            1 if body.disponible else 0,
            mecanico_id,
        ))
    
    return {"ok": True, "mensaje": "Mecánico actualizado ✅"}


# ── DELETE /api/mecanicos/{id} → soft delete ──────────────────────────────────

@router.delete("/{mecanico_id}")
def eliminar_mecanico(mecanico_id: int, authorization: str = Header(None)):
    """Desactiva lógicamente a un mecánico (requiere rol admin)."""
    require_admin(authorization)

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id_mecanico FROM mecanico WHERE id_mecanico = %s AND activo = 1", (mecanico_id,))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Mecánico no encontrado")

        cur.execute("UPDATE mecanico SET activo = 0 WHERE id_mecanico = %s", (mecanico_id,))

    return {"ok": True, "mensaje": "Mecánico desactivado ✅"}