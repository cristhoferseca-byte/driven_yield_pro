# app/routers/citas.py
# ─────────────────────────────────────────────────────────────────────────────
# CORRECCIONES vs versión anterior:
#
#  [CIT-1] _resolve_or_create_vehiculo: si body.vehiculo era "" y body.marca era
#          "" también, split(" ")[0] retornaba "" → se insertaba marca vacía en BD.
#          Se aplica un fallback a "Desconocido".
#
#  [CIT-2] _resolve_or_create_vehiculo: si body.placa era "" se generaba la
#          clave "SIN-PLACA" sin importar cuántas veces se llamara → múltiples
#          citas del mismo usuario creaban múltiples vehículos con placa "SIN-PLACA".
#          Ahora se busca por (marca, modelo, id_usuario) si no hay placa.
#
#  [CIT-3] _resolve_servicio: si el servicio no existía se usaba silenciosamente
#          id_servicio=1 sin avisar. Esto podía registrar citas con servicio
#          incorrecto sin que el usuario lo supiera. Se lanza 400 en su lugar.
#
#  [CIT-4] crear_cita: si no había mecánico disponible (mec=None), se usaba
#          id_mecanico=1 hardcodeado sin verificar que exista → FK violation.
#          Ahora se permite NULL si no hay mecánico (la columna debe ser nullable).
#
#  [CIT-5] update_estado: un cliente podía cambiar el estado a CUALQUIER valor
#          incluyendo "completada" o "confirmada", que solo debería poder poner
#          el admin. Se restringe a clientes únicamente el estado "cancelada".
#
#  [CIT-6] eliminar_cita: se borraba historial antes de verificar que la cita
#          existía y pertenecía al usuario. Si la cita no existía, rowcount=0
#          devolvía 404 pero el historial ya estaba potencialmente borrado.
#          Se verifica primero.
#
#  [CIT-7] hora: mismo problema que [ADM-3], se formatea timedelta → HH:MM.
#
#  [CIT-8] Envío de correo al crear cita (integración con email_service).
# ─────────────────────────────────────────────────────────────────────────────

import datetime as dt

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.security import get_current_user
from app.email_service import send_cita_confirmada
from app.google_calendar import crear_evento_cita, eliminar_evento_cita, actualizar_evento_cita
from app.routers.notificaciones import crear_notificacion

router = APIRouter(prefix="/api/citas", tags=["citas"])


# ── Schemas ───────────────────────────────────────────────────────────────────

class CitaBody(BaseModel):
    cliente:  str
    vehiculo: str = ""
    placa:    str = ""
    marca:    str = ""
    modelo:   str = ""
    anio:     Optional[str] = None
    color:    Optional[str] = None
    servicio: str
    fecha:    str
    hora:     str
    notas:    str = ""
    monto:    float = 0.0
    id_mecanico: Optional[int] = None

class EstadoBody(BaseModel):
    estado: str


# ── Helpers ───────────────────────────────────────────────────────────────────

def _format_hora(value) -> str:
    """[CIT-7] Convierte timedelta de MySQL → 'HH:MM'."""
    if value is None:
        return ""
    if isinstance(value, dt.timedelta):
        total = int(value.total_seconds())
        h, rem = divmod(total, 3600)
        m, _   = divmod(rem, 60)
        return f"{h:02d}:{m:02d}"
    return str(value)


def _format_cita(row: dict) -> dict:
    """Formatea la fecha y hora de un registro de cita para la serialización JSON."""
    if row.get("fecha"):
        row["fecha"] = str(row["fecha"])
    if "hora" in row:
        row["hora"] = _format_hora(row["hora"])
    return row


def _resolve_or_create_vehiculo(conn, uid: int, body: CitaBody) -> int:
    cur = conn.cursor()

    # [CIT-1] Fallbacks seguros para marca y modelo
    marca  = (body.marca  or body.vehiculo.split(" ")[0] if body.vehiculo else "").strip() or "Desconocido"
    modelo = (body.modelo or (" ".join(body.vehiculo.split(" ")[1:]) if body.vehiculo else "")).strip() or "N/A"
    placa  = body.placa.upper().strip() if body.placa else ""

    if placa:
        # Buscar por placa del usuario
        cur.execute(
            "SELECT id_vehiculo FROM vehiculo WHERE numero_de_placa = %s AND id_usuario = %s LIMIT 1",
            (placa, uid)
        )
        row = cur.fetchone()
        if row:
            return row["id_vehiculo"]
    else:
        # [CIT-2] Sin placa: buscar por marca+modelo+usuario para evitar duplicados
        cur.execute(
            """SELECT id_vehiculo FROM vehiculo
               WHERE marca = %s AND modelo = %s AND id_usuario = %s
               AND (numero_de_placa IS NULL OR numero_de_placa = 'SIN-PLACA')
               LIMIT 1""",
            (marca, modelo, uid)
        )
        row = cur.fetchone()
        if row:
            return row["id_vehiculo"]

    # Crear vehículo nuevo
    cur.execute(
        """INSERT INTO vehiculo (marca, modelo, año, color, numero_de_placa, id_usuario)
           VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_vehiculo""",
        (
            marca,
            modelo,
            body.anio  or "2024",
            body.color or "N/A",
            placa      or "SIN-PLACA",
            uid,
        )
    )
    return cur.fetchone()["id_vehiculo"]


def _resolve_servicio(conn, nombre: str):
    """Retorna (id_servicio, categoria) del servicio buscado por nombre."""
    cur = conn.cursor()
    cur.execute("SELECT id_servicio, categoria FROM servicio WHERE nombre = %s LIMIT 1", (nombre,))
    row = cur.fetchone()
    if not row:
        # [CIT-3] Error explícito — no silenciar con id=1
        raise HTTPException(status_code=400, detail=f"Servicio '{nombre}' no encontrado")
    return row["id_servicio"], row["categoria"]


def _seleccionar_mecanico_automatico(conn, categoria: str):
    """
    [CIT-9] Asignación automática de mecánico según el tipo de servicio.

    En vez de elegir un mecánico al azar entre todos los disponibles, se busca
    primero un mecánico cuya 'especialidad' coincida con la 'categoria' del
    servicio solicitado. Si ninguno coincide, se cae al comportamiento
    anterior (cualquier mecánico disponible al azar).
    """
    cur = conn.cursor()

    if categoria:
        categoria = categoria.strip()
        cur.execute(
            """SELECT id_mecanico FROM mecanico
               WHERE disponible = 1
                 AND especialidad IS NOT NULL
                 AND (especialidad LIKE %s OR %s LIKE CONCAT('%%', especialidad, '%%'))
               ORDER BY RAND() LIMIT 1""",
            (f"%{categoria}%", categoria)
        )
        mec = cur.fetchone()
        if mec:
            return mec["id_mecanico"]

    # Fallback: ningún mecánico con esa especialidad disponible -> cualquiera disponible
    cur.execute("SELECT id_mecanico FROM mecanico WHERE disponible = 1 ORDER BY RANDOM() LIMIT 1")
    mec = cur.fetchone()
    return mec["id_mecanico"] if mec else None


# ── GET /api/citas/disponibilidad ─────────────────────────────────────────────

@router.get("/disponibilidad")
def get_disponibilidad(fecha: str, authorization: str = Header(None)):
    """Retorna las horas disponibles para una fecha dada (08:00 a 17:00)."""
    # Se omiten horas ya agendadas que no estén canceladas
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT hora FROM cita WHERE fecha = %s AND estado != 'cancelada'",
            (fecha,)
        )
        rows = cur.fetchall()
        
    horas_ocupadas = set(_format_hora(r["hora"]) for r in rows if r["hora"])
    
    todas_las_horas = [
        "08:00", "09:00", "10:00", "11:00", 
        "12:00", "13:00", "14:00", "15:00", 
        "16:00", "17:00"
    ]
    
    disponibles = [h for h in todas_las_horas if h not in horas_ocupadas]
    return disponibles

@router.get("/mecanicos")
def get_mecanicos_disponibles(authorization: str = Header(None)):
    """Retorna la lista de mecánicos que actualmente tienen disponibilidad marcada."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id_mecanico, nombre, especialidad FROM mecanico WHERE disponible = 1")
        rows = cur.fetchall()
    return rows




# ── GET /api/citas ────────────────────────────────────────────────────────────

@router.get("")
def get_mis_citas(authorization: str = Header(None)):
    """Obtiene la lista de citas activas asociadas al cliente autenticado."""
    payload = get_current_user(authorization)
    uid = payload["sub"]
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT
                c.id_cita                      AS id,
                u.nombre                        AS cliente,
                u.email,
                CONCAT(v.marca, ' ', v.modelo) AS vehiculo,
                v.numero_de_placa               AS placa,
                s.nombre                        AS servicio,
                c.fecha,
                c.hora,
                c.notas,
                c.monto,
                c.estado
            FROM cita c
            LEFT JOIN usuario  u ON c.id_usuario  = u.id_usuario
            LEFT JOIN vehiculo v ON c.id_vehiculo = v.id_vehiculo
            LEFT JOIN servicio s ON c.id_servicio = s.id_servicio
            WHERE c.id_usuario = %s AND c.estado != 'cancelada'
            ORDER BY c.fecha DESC, c.hora DESC
        """, (uid,))
        rows = cur.fetchall()
    return [_format_cita(r) for r in rows]


# ── POST /api/citas ───────────────────────────────────────────────────────────

@router.post("")
def crear_cita(body: CitaBody, authorization: str = Header(None)):
    """Crea y registra una nueva cita para el cliente autenticado, asignando mecánico y sincronizando."""
    payload = get_current_user(authorization)
    uid = payload["sub"]

    with get_db() as conn:
        vid = _resolve_or_create_vehiculo(conn, uid, body)
        sid, categoria = _resolve_servicio(conn, body.servicio)   # [CIT-3] lanza 400 si no existe

        # [CIT-4][CIT-9] Mecánico: si no se eligió uno manualmente, se asigna
        # automáticamente según la categoría del servicio.
        mid = body.id_mecanico
        cur = conn.cursor()
        if not mid:
            mid = _seleccionar_mecanico_automatico(conn, categoria)

        cur.execute(
            """INSERT INTO cita
               (fecha, hora, notas, monto, estado, id_usuario, id_vehiculo, id_servicio, id_mecanico)
               VALUES (%s, %s, %s, %s, 'pendiente', %s, %s, %s, %s) RETURNING id_cita""",
            (body.fecha, body.hora, body.notas, body.monto, uid, vid, sid, mid)
        )
        new_id = cur.fetchone()["id_cita"]

        # Leer la cita recién creada con JOINs
        cur.execute("""
            SELECT
                c.id_cita                      AS id,
                u.nombre                        AS cliente,
                u.email,
                CONCAT(v.marca, ' ', v.modelo) AS vehiculo,
                v.numero_de_placa               AS placa,
                s.nombre                        AS servicio,
                c.fecha, c.hora, c.notas, c.monto, c.estado
            FROM cita c
            LEFT JOIN usuario  u ON c.id_usuario  = u.id_usuario
            LEFT JOIN vehiculo v ON c.id_vehiculo = v.id_vehiculo
            LEFT JOIN servicio s ON c.id_servicio = s.id_servicio
            WHERE c.id_cita = %s
        """, (new_id,))
        cita = cur.fetchone()

        # [CIT-9] Notificación in-app (dentro del mismo bloque/conexión)
        crear_notificacion(
            conn,
            id_usuario=uid,
            titulo="Cita agendada con éxito",
            mensaje=f"Tu cita de {cita['servicio']} quedó registrada para el {cita['fecha']} a las {_format_hora(cita['hora'])}.",
            tipo="cita_creada",
            id_referencia=new_id,
        )

    cita = _format_cita(cita)

    # [CIT-8] Notificación por correo (no bloqueante)
    send_cita_confirmada(
        cita["email"],
        cita["cliente"],
        cita["servicio"],
        cita["fecha"],
        cita["hora"],
    )

    # Integración con Google Calendar
    try:
        crear_evento_cita(cita)
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Fallo al crear el evento de Google Calendar de forma silenciosa: {e}")

    return {"ok": True, "cita": cita}


# ── PUT /api/citas/{id}/estado ────────────────────────────────────────────────

@router.put("/{cita_id}/estado")
@router.patch("/{cita_id}/estado")
def update_estado(cita_id: int, body: EstadoBody, authorization: str = Header(None)):
    """Actualiza el estado de una cita (clientes solo pueden cancelar su propia cita)."""
    payload = get_current_user(authorization)
    uid  = payload["sub"]
    role = payload.get("role")

    estados_validos = {"pendiente", "confirmada", "completada", "cancelada"}
    if body.estado not in estados_validos:
        raise HTTPException(status_code=400, detail="Estado inválido")

    # [CIT-5] Clientes solo pueden cancelar sus propias citas
    if role != "admin" and body.estado != "cancelada":
        raise HTTPException(
            status_code=403,
            detail="Los clientes solo pueden cancelar citas"
        )

    with get_db() as conn:
        cur = conn.cursor()
        # Recuperar cita para Google Calendar
        cur.execute("""
            SELECT c.fecha, c.hora, u.nombre AS cliente
            FROM cita c
            LEFT JOIN usuario u ON c.id_usuario = u.id_usuario
            WHERE c.id_cita = %s
        """, (cita_id,))
        cita_data = cur.fetchone()

        if role == "admin":
            cur.execute(
                "UPDATE cita SET estado = %s WHERE id_cita = %s",
                (body.estado, cita_id)
            )
        else:
            cur.execute(
                "UPDATE cita SET estado = %s WHERE id_cita = %s AND id_usuario = %s",
                (body.estado, cita_id, uid)
            )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Cita no encontrada o sin permiso")
            
        if body.estado == "cancelada" and cita_data:
            cita_data = _format_cita(cita_data)
            try:
                eliminar_evento_cita(cita_data)
            except:
                pass

    return {"ok": True}


# ── PUT /api/citas/{id} (Editar Cita) ─────────────────────────────────────────

@router.put("/{cita_id}")
def editar_cita(cita_id: int, body: CitaBody, authorization: str = Header(None)):
    """Modifica los detalles de una cita existente con validación de permisos."""
    payload = get_current_user(authorization)
    uid  = payload["sub"]
    role = payload.get("role")

    with get_db() as conn:
        cur = conn.cursor()
        # Verificar pertenencia y obtener datos antiguos para Google Calendar
        cur.execute("""
            SELECT c.fecha, c.hora, u.nombre AS cliente, c.id_usuario
            FROM cita c
            LEFT JOIN usuario u ON c.id_usuario = u.id_usuario
            WHERE c.id_cita = %s
        """, (cita_id,))
        cita_antigua = cur.fetchone()
        
        if not cita_antigua or (role != "admin" and cita_antigua["id_usuario"] != uid):
            raise HTTPException(status_code=404, detail="Cita no encontrada o sin permiso")

        vid = _resolve_or_create_vehiculo(conn, uid if role != "admin" else cita_antigua["id_usuario"], body)
        sid, categoria = _resolve_servicio(conn, body.servicio)
        mid = body.id_mecanico or _seleccionar_mecanico_automatico(conn, categoria)

        cur.execute(
            """UPDATE cita 
               SET fecha=%s, hora=%s, notas=%s, monto=%s, id_vehiculo=%s, id_servicio=%s, id_mecanico=%s
               WHERE id_cita=%s""",
            (body.fecha, body.hora, body.notas, body.monto, vid, sid, mid, cita_id)
        )
        
        cita_antigua = _format_cita(cita_antigua)
        cita_nueva = {
            "cliente": cita_antigua["cliente"],
            "fecha": body.fecha,
            "hora": body.hora,
            "servicio": body.servicio
        }
        try:
            actualizar_evento_cita(cita_antigua, cita_nueva)
        except:
            pass

    return {"ok": True}


# ── DELETE /api/citas/{id} ────────────────────────────────────────────────────

@router.delete("/{cita_id}")
def eliminar_cita(cita_id: int, authorization: str = Header(None)):
    """Elimina permanentemente una cita y su historial relacionado."""
    payload = get_current_user(authorization)
    uid  = payload["sub"]
    role = payload.get("role")

    with get_db() as conn:
        cur = conn.cursor()

        # [CIT-6] Verificar existencia y pertenencia ANTES de borrar historial
        if role == "admin":
            cur.execute("""
                SELECT c.id_cita, c.fecha, c.hora, u.nombre AS cliente 
                FROM cita c LEFT JOIN usuario u ON c.id_usuario = u.id_usuario 
                WHERE c.id_cita = %s
            """, (cita_id,))
        else:
            cur.execute("""
                SELECT c.id_cita, c.fecha, c.hora, u.nombre AS cliente 
                FROM cita c LEFT JOIN usuario u ON c.id_usuario = u.id_usuario 
                WHERE c.id_cita = %s AND c.id_usuario = %s
            """, (cita_id, uid))
            
        cita_data = cur.fetchone()
        if not cita_data:
            raise HTTPException(status_code=404, detail="Cita no encontrada o sin permiso")

        cur.execute("DELETE FROM historial_cita WHERE id_cita = %s", (cita_id,))
        cur.execute("DELETE FROM cita WHERE id_cita = %s", (cita_id,))
        
        cita_data = _format_cita(cita_data)
        try:
            eliminar_evento_cita(cita_data)
        except:
            pass

    return {"ok": True}
