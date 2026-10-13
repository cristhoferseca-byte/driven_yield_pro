# app/routers/servicios.py
# ─────────────────────────────────────────────────────────────────────────────
# Sin bugs críticos en el original, pero se agrega:
#  - Conversión explícita de campos Decimal (precio) a float para JSON seguro.
#  - Conversión de campo duracion (puede venir como timedelta) a string.
# ─────────────────────────────────────────────────────────────────────────────

import datetime as dt
from decimal import Decimal

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel

from app.database import get_db
from app.security import require_admin

router = APIRouter(prefix="/api/servicios", tags=["servicios"])


# ── Schema ────────────────────────────────────────────────────────────────────

class ServicioBody(BaseModel):
    """Esquema para la creación y actualización de servicios del taller."""
    nombre: str
    categoria: str
    precio: float
    duracion: str
    descripcion: str = ""
    imagen: str = ""


def _format_servicio(row: dict) -> dict:
    """Formatea los campos del servicio convirtiendo Decimal a float y duración a string."""
    # Decimal → float (evita error de serialización JSON)
    if isinstance(row.get("precio"), Decimal):
        row["precio"] = float(row["precio"])
    # timedelta → string legible (e.g. "01:30")
    dur = row.get("duracion")
    if isinstance(dur, dt.timedelta):
        total = int(dur.total_seconds())
        h, rem = divmod(total, 3600)
        m, _   = divmod(rem, 60)
        row["duracion"] = f"{h:02d}:{m:02d}"
    return row


@router.get("")
def get_servicios():
    """Retorna la lista de todos los servicios automotrices activos."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id_servicio AS id, nombre, categoria, precio, duracion, descripcion, imagen "
            "FROM servicio WHERE activo = 1 ORDER BY categoria, nombre"
        )
        rows = cur.fetchall()
    return [_format_servicio(r) for r in rows]

@router.post("")
def crear_servicio(body: ServicioBody, authorization: str = Header(None)):
    """Crea un nuevo servicio en el catálogo (requiere rol admin)."""
    require_admin(authorization)
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO servicio (nombre, categoria, precio, duracion, descripcion, imagen, activo) "
            "VALUES (%s, %s, %s, %s, %s, %s, 1) RETURNING id_servicio",
            (body.nombre, body.categoria, body.precio, body.duracion, body.descripcion, body.imagen)
        )
        new_id = cur.fetchone()["id_servicio"]
    return {"id": new_id, **body.dict()}


@router.put("/{servicio_id}")
def actualizar_servicio(servicio_id: int, body: ServicioBody, authorization: str = Header(None)):
    """Actualiza la información de un servicio existente (requiere rol admin)."""
    require_admin(authorization)
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id_servicio FROM servicio WHERE id_servicio = %s", (servicio_id,))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Servicio no encontrado")
        cur.execute(
            "UPDATE servicio SET nombre=%s, categoria=%s, precio=%s, duracion=%s, "
            "descripcion=%s, imagen=%s WHERE id_servicio=%s",
            (body.nombre, body.categoria, body.precio, body.duracion, body.descripcion, body.imagen, servicio_id)
        )
        conn.commit()
    return {"id": servicio_id, **body.dict()}


@router.delete("/{servicio_id}")
def eliminar_servicio(servicio_id: int, authorization: str = Header(None)):
    """Desactiva un servicio del catálogo mediante baja lógica (requiere rol admin)."""
    require_admin(authorization)
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id_servicio FROM servicio WHERE id_servicio = %s", (servicio_id,))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Servicio no encontrado")
        cur.execute("UPDATE servicio SET activo = 0 WHERE id_servicio = %s", (servicio_id,))
        conn.commit()
    return {"ok": True}


@router.post("/seed")
def seed_servicios():
    """Siembra los servicios base iniciales en caso de no existir."""
    nuevos = [
        ("Mantenimiento de Motor", "Mantenimiento", 150000, "120 min", "Revisión general y afinación del motor"),
        ("Cambio de Aceite y Filtro", "Mantenimiento", 80000, "45 min", "Cambio de aceite multigrado y filtro nuevo"),
        ("Arreglo y Cambio de Bujías", "Mantenimiento", 60000, "60 min", "Reemplazo de bujías y limpieza de cables"),
        ("Alineación y Balanceo", "Llantas", 50000, "45 min", "Alineación sencilla y balanceo de 4 ruedas"),
        ("Revisión Sistema Eléctrico", "Diagnóstico", 40000, "60 min", "Revisión de batería, alternador y luces"),
        ("Cambio Pastillas de Freno", "Frenos", 120000, "90 min", "Reemplazo de pastillas delanteras/traseras y purga"),
        ("Lavado y Aspirado General", "Estética", 35000, "40 min", "Lavado exterior con cera y aspirado profundo de interiores"),
        ("Revisión General de Viaje", "Diagnóstico", 50000, "60 min", "Chequeo de 20 puntos de seguridad antes de viajar")
    ]
    with get_db() as conn:
        cur = conn.cursor()
        for n, c, p, d, desc in nuevos:
            cur.execute("SELECT id_servicio FROM servicio WHERE nombre = %s", (n,))
            if not cur.fetchone():
                cur.execute(
                    "INSERT INTO servicio (nombre, categoria, precio, duracion, descripcion, activo) VALUES (%s, %s, %s, %s, %s, 1)",
                    (n, c, p, d, desc)
                )
        conn.commit()
    return {"ok": True}