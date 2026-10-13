# app/routers/practica.py
# ─────────────────────────────────────────────────────────────────────────────
# Endpoints implementados como práctica guiada (Mini Práctica — ADSO 2026)
# Proyecto: driven_yield | SENA CEET | Mayo 2026
#
# PARTE 1 — PATH params:
#   1. GET /vehiculos/{id}             → vehículo por ID
#   2. GET /clientes/{id}/citas        → citas de un cliente específico
#   3. GET /ordenes/{id}               → orden (cita) por ID
#   4. GET /mecanicos/{id}/servicios   → servicios asignados a un mecánico
#   5. GET /ordenes/{id}/factura       → factura/resumen de una orden
#
# PARTE 2 — QUERY params:
#   6.  GET /citas?fecha=&estado=      → filtrar citas por fecha y estado
#   7.  GET /productos?orden=&direccion= → productos/servicios ordenados
#   8.  GET /clientes?page=&limit=     → paginar lista de clientes
#   9.  GET /ordenes?estado=&mecanico_id= → filtrar órdenes por estado y mecánico
#   10. GET /vehiculos?marca=&modelo=  → buscar vehículos por marca/modelo
# ─────────────────────────────────────────────────────────────────────────────

import datetime as dt
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, HTTPException, Header, Query
from app.database import get_db
from app.security import get_current_user, require_admin

router = APIRouter(tags=["practica-guiada"])


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _fmt_hora(value) -> str:
    """Convierte objeto timedelta o datetime al formato legible HH:MM."""
    if value is None:
        return ""
    if isinstance(value, dt.timedelta):
        total = int(value.total_seconds())
        h, rem = divmod(total, 3600)
        m, _   = divmod(rem, 60)
        return f"{h:02d}:{m:02d}"
    return str(value)

def _fmt_decimal(value) -> float | None:
    """Convierte valores de tipo Decimal a flotante estándar para serialización JSON segura."""
    if isinstance(value, Decimal):
        return float(value)
    return value

def _fmt_cita(row: dict) -> dict:
    """Aplica formato adecuado y serialización a fechas, horas y montos en los registros de citas."""
    if row.get("fecha"):
        row["fecha"] = str(row["fecha"])
    if "hora" in row:
        row["hora"] = _fmt_hora(row["hora"])
    if "monto" in row:
        row["monto"] = _fmt_decimal(row["monto"])
    return row


# ═════════════════════════════════════════════════════════════════════════════
# PARTE 1 — PATH params
# ═════════════════════════════════════════════════════════════════════════════

# ── 1. GET /vehiculos/{id} ────────────────────────────────────────────────────
@router.get("/vehiculos/{id}")
def get_vehiculo_por_id(id: int, authorization: str = Header(None)):
    """Obtener un vehículo por su ID. Solo el dueño o un admin pueden verlo."""
    payload = get_current_user(authorization)
    uid  = payload["sub"]
    role = payload.get("role", "cliente")

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT v.id_vehiculo AS id, v.marca, v.modelo, v.año,
                      v.color, v.numero_de_placa AS placa,
                      u.nombre AS propietario, u.email
               FROM vehiculo v
               LEFT JOIN usuario u ON v.id_usuario = u.id_usuario
               WHERE v.id_vehiculo = %s""",
            (id,)
        )
        row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    # Clientes solo pueden ver sus propios vehículos
    if role != "admin":
        # Re-consultar para verificar propietario sin exponer datos
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id_vehiculo FROM vehiculo WHERE id_vehiculo = %s AND id_usuario = %s",
                (id, uid)
            )
            if not cur.fetchone():
                raise HTTPException(status_code=403, detail="Sin permiso para ver este vehículo")

    return row


# ── 2. GET /clientes/{id}/citas ───────────────────────────────────────────────
@router.get("/clientes/{id}/citas")
def get_citas_de_cliente(id: int, authorization: str = Header(None)):
    """Citas de un cliente específico. Admin ve todas; cliente solo las propias."""
    payload = get_current_user(authorization)
    uid  = payload["sub"]
    role = payload.get("role", "cliente")

    # Cliente solo puede ver sus propias citas
    if role != "admin" and uid != id:
        raise HTTPException(status_code=403, detail="Sin permiso para ver estas citas")

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT c.id_cita AS id,
                   s.nombre  AS servicio,
                   CONCAT(v.marca, ' ', v.modelo) AS vehiculo,
                   v.numero_de_placa AS placa,
                   c.fecha, c.hora, c.estado, c.monto,
                   m.nombre AS mecanico
            FROM cita c
            LEFT JOIN servicio  s ON c.id_servicio = s.id_servicio
            LEFT JOIN vehiculo  v ON c.id_vehiculo  = v.id_vehiculo
            LEFT JOIN mecanico  m ON c.id_mecanico  = m.id_mecanico
            WHERE c.id_usuario = %s
            ORDER BY c.fecha DESC, c.hora DESC
        """, (id,))
        rows = cur.fetchall()

    return [_fmt_cita(r) for r in rows]


# ── 3. GET /ordenes/{id} ──────────────────────────────────────────────────────
@router.get("/ordenes/{id}")
def get_orden_por_id(id: int, authorization: str = Header(None)):
    """Obtener una orden de trabajo (cita) por su ID."""
    payload = get_current_user(authorization)
    uid  = payload["sub"]
    role = payload.get("role", "cliente")

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT c.id_cita AS id,
                   u.nombre  AS cliente, u.email,
                   CONCAT(v.marca, ' ', v.modelo) AS vehiculo,
                   v.numero_de_placa AS placa,
                   s.nombre  AS servicio,
                   c.fecha, c.hora, c.notas,
                   c.monto, c.estado,
                   m.nombre  AS mecanico
            FROM cita c
            LEFT JOIN usuario   u ON c.id_usuario  = u.id_usuario
            LEFT JOIN vehiculo  v ON c.id_vehiculo  = v.id_vehiculo
            LEFT JOIN servicio  s ON c.id_servicio  = s.id_servicio
            LEFT JOIN mecanico  m ON c.id_mecanico  = m.id_mecanico
            WHERE c.id_cita = %s
        """, (id,))
        row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    if role != "admin" and row.get("email") != payload.get("nombre"):
        # Verificar por id_usuario
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id_cita FROM cita WHERE id_cita = %s AND id_usuario = %s", (id, uid))
            if not cur.fetchone():
                raise HTTPException(status_code=403, detail="Sin permiso para ver esta orden")

    return _fmt_cita(row)


# ── 4. GET /mecanicos/{id}/servicios ─────────────────────────────────────────
@router.get("/mecanicos/{id}/servicios")
def get_servicios_de_mecanico(id: int, authorization: str = Header(None)):
    """Servicios (citas) asignados a un mecánico. Solo admin."""
    require_admin(authorization)

    with get_db() as conn:
        cur = conn.cursor()

        # Verificar que el mecánico existe
        cur.execute("SELECT nombre, disponible FROM mecanico WHERE id_mecanico = %s", (id,))
        mec = cur.fetchone()
        if not mec:
            raise HTTPException(status_code=404, detail="Mecánico no encontrado")

        cur.execute("""
            SELECT c.id_cita AS id,
                   u.nombre  AS cliente,
                   CONCAT(v.marca, ' ', v.modelo) AS vehiculo,
                   s.nombre  AS servicio,
                   c.fecha, c.hora, c.estado, c.monto
            FROM cita c
            LEFT JOIN usuario   u ON c.id_usuario  = u.id_usuario
            LEFT JOIN vehiculo  v ON c.id_vehiculo  = v.id_vehiculo
            LEFT JOIN servicio  s ON c.id_servicio  = s.id_servicio
            WHERE c.id_mecanico = %s
            ORDER BY c.fecha DESC
        """, (id,))
        citas = cur.fetchall()

    return {
        "mecanico": {
            "id":         id,
            "nombre":     mec["nombre"],
            "disponible": bool(mec["disponible"]),
        },
        "total_servicios": len(citas),
        "servicios": [_fmt_cita(c) for c in citas],
    }


# ── 5. GET /ordenes/{id}/factura ──────────────────────────────────────────────
@router.get("/ordenes/{id}/factura")
def get_factura_de_orden(id: int, authorization: str = Header(None)):
    """Retorna el resumen/factura de una orden. Responde en JSON."""
    payload = get_current_user(authorization)
    uid  = payload["sub"]
    role = payload.get("role", "cliente")

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT c.id_cita AS id_orden,
                   u.nombre  AS cliente, u.email,
                   CONCAT(v.marca, ' ', v.modelo) AS vehiculo,
                   v.numero_de_placa AS placa,
                   s.nombre  AS servicio,
                   s.precio  AS precio_servicio,
                   c.fecha, c.hora,
                   c.monto   AS total,
                   c.estado,
                   m.nombre  AS mecanico
            FROM cita c
            LEFT JOIN usuario   u ON c.id_usuario  = u.id_usuario
            LEFT JOIN vehiculo  v ON c.id_vehiculo  = v.id_vehiculo
            LEFT JOIN servicio  s ON c.id_servicio  = s.id_servicio
            LEFT JOIN mecanico  m ON c.id_mecanico  = m.id_mecanico
            WHERE c.id_cita = %s
        """, (id,))
        row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    # Clientes solo ven su propia factura
    if role != "admin":
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id_cita FROM cita WHERE id_cita = %s AND id_usuario = %s", (id, uid))
            if not cur.fetchone():
                raise HTTPException(status_code=403, detail="Sin permiso para ver esta factura")

    row = _fmt_cita(row)
    row["precio_servicio"] = _fmt_decimal(row.get("precio_servicio"))
    row["total"] = _fmt_decimal(row.get("total"))

    return {
        "factura": {
            "numero":          f"FAC-{id:05d}",
            "id_orden":        row["id_orden"],
            "fecha_emision":   str(dt.date.today()),
            "estado_orden":    row["estado"],
        },
        "cliente": {
            "nombre": row["cliente"],
            "email":  row["email"],
        },
        "vehiculo": {
            "descripcion": row["vehiculo"],
            "placa":       row["placa"],
        },
        "detalle": {
            "servicio":         row["servicio"],
            "mecanico":         row["mecanico"],
            "fecha_servicio":   row["fecha"],
            "hora_servicio":    row["hora"],
            "precio_unitario":  row["precio_servicio"],
            "total":            row["total"],
        },
        "nota": "Este documento es un resumen en JSON. Generar PDF bajo petición."
    }


# ═════════════════════════════════════════════════════════════════════════════
# PARTE 2 — QUERY params
# ═════════════════════════════════════════════════════════════════════════════

# ── 6. GET /citas?fecha=&estado= ──────────────────────────────────────────────
@router.get("/citas")
def filtrar_citas(
    fecha:     Optional[str] = Query(None, description="Fecha exacta YYYY-MM-DD"),
    estado:    Optional[str] = Query(None, description="pendiente|confirmada|completada|cancelada"),
    authorization: str = Header(None),
):
    """Filtrar citas por fecha y/o estado. Admin ve todas; cliente solo las propias."""
    payload = get_current_user(authorization)
    uid  = payload["sub"]
    role = payload.get("role", "cliente")

    conditions = []
    params     = []

    if role != "admin":
        conditions.append("c.id_usuario = %s")
        params.append(uid)

    if fecha:
        conditions.append("c.fecha = %s")
        params.append(fecha)

    if estado:
        estados_validos = {"pendiente", "confirmada", "completada", "cancelada"}
        if estado not in estados_validos:
            raise HTTPException(status_code=400, detail=f"Estado inválido. Usa: {', '.join(estados_validos)}")
        conditions.append("c.estado = %s")
        params.append(estado)

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(f"""
            SELECT c.id_cita AS id,
                   u.nombre  AS cliente,
                   s.nombre  AS servicio,
                   CONCAT(v.marca, ' ', v.modelo) AS vehiculo,
                   c.fecha, c.hora, c.estado, c.monto
            FROM cita c
            LEFT JOIN usuario  u ON c.id_usuario  = u.id_usuario
            LEFT JOIN servicio s ON c.id_servicio = s.id_servicio
            LEFT JOIN vehiculo v ON c.id_vehiculo = v.id_vehiculo
            {where}
            ORDER BY c.fecha DESC, c.hora DESC
        """, params)
        rows = cur.fetchall()

    return {
        "filtros": {"fecha": fecha, "estado": estado},
        "total":   len(rows),
        "citas":   [_fmt_cita(r) for r in rows],
    }


# ── 7. GET /productos?orden=precio&direccion=asc ──────────────────────────────
@router.get("/productos")
def listar_productos(
    orden:     str = Query("nombre", description="Campo de ordenamiento: nombre|precio|categoria"),
    direccion: str = Query("asc",    description="asc | desc"),
):
    """Listar servicios/productos ordenados. Público (no requiere auth)."""
    campos_validos = {"nombre", "precio", "categoria"}
    if orden not in campos_validos:
        raise HTTPException(status_code=400, detail=f"Campo inválido. Usa: {', '.join(campos_validos)}")

    dir_sql = "ASC" if direccion.lower() != "desc" else "DESC"

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(f"""
            SELECT id_servicio AS id, nombre, categoria, precio, duracion, descripcion
            FROM servicio
            WHERE activo = 1
            ORDER BY {orden} {dir_sql}
        """)
        rows = cur.fetchall()

    for r in rows:
        r["precio"] = _fmt_decimal(r.get("precio"))
        if isinstance(r.get("duracion"), dt.timedelta):
            total = int(r["duracion"].total_seconds())
            h, rem = divmod(total, 3600)
            m, _ = divmod(rem, 60)
            r["duracion"] = f"{h:02d}:{m:02d}"

    return {
        "orden":     orden,
        "direccion": dir_sql,
        "total":     len(rows),
        "productos": rows,
    }


# ── 8. GET /clientes?page=&limit= ────────────────────────────────────────────
@router.get("/clientes")
def listar_clientes(
    page:  int = Query(1,  ge=1,   description="Número de página (desde 1)"),
    limit: int = Query(10, ge=1, le=100, description="Resultados por página (máx 100)"),
    authorization: str = Header(None),
):
    """Paginar lista de clientes. Solo admin."""
    require_admin(authorization)

    offset = (page - 1) * limit

    with get_db() as conn:
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) AS total FROM usuario")
        total = cur.fetchone()["total"]

        cur.execute("""
            SELECT id_usuario AS id, nombre, username, email, telefono
            FROM usuario
            ORDER BY nombre
            LIMIT %s OFFSET %s
        """, (limit, offset))
        rows = cur.fetchall()

    total_pages = (total + limit - 1) // limit

    return {
        "paginacion": {
            "page":        page,
            "limit":       limit,
            "total":       total,
            "total_pages": total_pages,
            "has_next":    page < total_pages,
            "has_prev":    page > 1,
        },
        "clientes": rows,
    }


# ── 9. GET /ordenes?estado=&mecanico_id= ──────────────────────────────────────
@router.get("/ordenes")
def filtrar_ordenes(
    estado:      Optional[str] = Query(None, description="Estado de la orden"),
    mecanico_id: Optional[int] = Query(None, description="ID del mecánico asignado"),
    authorization: str = Header(None),
):
    """Filtrar órdenes por estado y/o mecánico. Solo admin."""
    require_admin(authorization)

    conditions = []
    params     = []

    if estado:
        estados_validos = {"pendiente", "confirmada", "completada", "cancelada"}
        if estado not in estados_validos:
            raise HTTPException(status_code=400, detail=f"Estado inválido. Usa: {', '.join(estados_validos)}")
        conditions.append("c.estado = %s")
        params.append(estado)

    if mecanico_id:
        conditions.append("c.id_mecanico = %s")
        params.append(mecanico_id)

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(f"""
            SELECT c.id_cita AS id,
                   u.nombre  AS cliente,
                   CONCAT(v.marca, ' ', v.modelo) AS vehiculo,
                   s.nombre  AS servicio,
                   m.nombre  AS mecanico,
                   c.fecha, c.hora, c.estado, c.monto
            FROM cita c
            LEFT JOIN usuario   u ON c.id_usuario  = u.id_usuario
            LEFT JOIN vehiculo  v ON c.id_vehiculo  = v.id_vehiculo
            LEFT JOIN servicio  s ON c.id_servicio  = s.id_servicio
            LEFT JOIN mecanico  m ON c.id_mecanico  = m.id_mecanico
            {where}
            ORDER BY c.fecha DESC, c.hora DESC
        """, params)
        rows = cur.fetchall()

    return {
        "filtros": {"estado": estado, "mecanico_id": mecanico_id},
        "total":   len(rows),
        "ordenes": [_fmt_cita(r) for r in rows],
    }


# ── 10. GET /vehiculos?marca=&modelo= ────────────────────────────────────────
@router.get("/vehiculos")
def buscar_vehiculos(
    marca:  Optional[str] = Query(None, description="Marca del vehículo (ej: Toyota)"),
    modelo: Optional[str] = Query(None, description="Modelo del vehículo (ej: Corolla)"),
    authorization: str = Header(None),
):
    """Buscar vehículos por marca y/o modelo. Admin ve todos; cliente solo los suyos."""
    payload = get_current_user(authorization)
    uid  = payload["sub"]
    role = payload.get("role", "cliente")

    conditions = []
    params     = []

    if role != "admin":
        conditions.append("v.id_usuario = %s")
        params.append(uid)

    if marca:
        conditions.append("v.marca LIKE %s")
        params.append(f"%{marca}%")

    if modelo:
        conditions.append("v.modelo LIKE %s")
        params.append(f"%{modelo}%")

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(f"""
            SELECT v.id_vehiculo AS id,
                   v.marca, v.modelo, v.año, v.color,
                   v.numero_de_placa AS placa,
                   u.nombre AS propietario
            FROM vehiculo v
            LEFT JOIN usuario u ON v.id_usuario = u.id_usuario
            {where}
            ORDER BY v.marca, v.modelo
        """, params)
        rows = cur.fetchall()

    return {
        "filtros": {"marca": marca, "modelo": modelo},
        "total":   len(rows),
        "vehiculos": rows,
    }
