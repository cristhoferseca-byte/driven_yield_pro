# app/routers/notificaciones.py
# ─────────────────────────────────────────────────────────────────────────────
# Notificaciones in-app. Se crean automáticamente (ver crear_notificacion,
# llamada desde citas.py al insertar una cita con éxito) y el frontend las
# consulta/marca como leídas mediante estos endpoints.
# ─────────────────────────────────────────────────────────────────────────────

from fastapi import APIRouter, HTTPException, Header

from app.database import get_db
from app.security import get_current_user

router = APIRouter(prefix="/api/notificaciones", tags=["notificaciones"])


# ── DDL (Postgres) ────────────────────────────────────────────────────────────

def _ensure_tabla(cur) -> None:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notificacion (
            id_notificacion SERIAL PRIMARY KEY,
            id_usuario INT NOT NULL REFERENCES usuario(id_usuario) ON DELETE CASCADE,
            tipo VARCHAR(50) NOT NULL DEFAULT 'cita_creada',
            titulo VARCHAR(150) NOT NULL,
            mensaje VARCHAR(500) NOT NULL,
            id_referencia INT,
            leida BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_notificacion_usuario
        ON notificacion(id_usuario, leida)
    """)


# ── Helper reutilizable desde otros routers ───────────────────────────────────

def crear_notificacion(
    conn,
    id_usuario: int,
    titulo: str,
    mensaje: str,
    tipo: str = "cita_creada",
    id_referencia: int | None = None,
) -> None:
    """
    Inserta una notificación. No lanza excepción hacia arriba si falla:
    una notificación no debe tumbar el flujo principal (ej. creación de cita).
    Debe llamarse DENTRO del mismo `with get_db() as conn:` de la operación
    principal, antes de que el bloque cierre la conexión.
    """
    try:
        cur = conn.cursor()
        _ensure_tabla(cur)
        cur.execute(
            """INSERT INTO notificacion (id_usuario, tipo, titulo, mensaje, id_referencia)
               VALUES (%s, %s, %s, %s, %s)""",
            (id_usuario, tipo, titulo, mensaje, id_referencia)
        )
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"No se pudo crear notificación: {e}")


# ── GET /api/notificaciones ───────────────────────────────────────────────────
# Lista las notificaciones del usuario autenticado (más recientes primero).

@router.get("")
def listar_notificaciones(
    solo_no_leidas: bool = False,
    authorization: str = Header(None),
):
    payload = get_current_user(authorization)
    uid = payload["sub"]

    with get_db() as conn:
        cur = conn.cursor()
        _ensure_tabla(cur)

        query = """
            SELECT id_notificacion AS id, tipo, titulo, mensaje,
                   id_referencia, leida, created_at
            FROM notificacion
            WHERE id_usuario = %s
        """
        params = [uid]
        if solo_no_leidas:
            query += " AND leida = FALSE"
        query += " ORDER BY created_at DESC LIMIT 100"

        cur.execute(query, params)
        rows = cur.fetchall()

        cur.execute(
            "SELECT COUNT(*) AS total FROM notificacion WHERE id_usuario = %s AND leida = FALSE",
            (uid,)
        )
        no_leidas = cur.fetchone()["total"]

    for r in rows:
        if r.get("created_at"):
            r["created_at"] = str(r["created_at"])

    return {"ok": True, "no_leidas": no_leidas, "notificaciones": rows}


# ── PUT /api/notificaciones/{id}/leer ─────────────────────────────────────────
# Marca una notificación puntual como leída (solo si pertenece al usuario).

@router.put("/{notif_id}/leer")
def marcar_leida(notif_id: int, authorization: str = Header(None)):
    payload = get_current_user(authorization)
    uid = payload["sub"]

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE notificacion SET leida = TRUE WHERE id_notificacion = %s AND id_usuario = %s",
            (notif_id, uid)
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Notificación no encontrada")

    return {"ok": True}


# ── PUT /api/notificaciones/leer-todas ────────────────────────────────────────

@router.put("/leer-todas")
def marcar_todas_leidas(authorization: str = Header(None)):
    payload = get_current_user(authorization)
    uid = payload["sub"]

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE notificacion SET leida = TRUE WHERE id_usuario = %s AND leida = FALSE",
            (uid,)
        )

    return {"ok": True}


# ── DELETE /api/notificaciones/{id} ───────────────────────────────────────────

@router.delete("/{notif_id}")
def eliminar_notificacion(notif_id: int, authorization: str = Header(None)):
    payload = get_current_user(authorization)
    uid = payload["sub"]

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM notificacion WHERE id_notificacion = %s AND id_usuario = %s",
            (notif_id, uid)
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Notificación no encontrada")

    return {"ok": True}
