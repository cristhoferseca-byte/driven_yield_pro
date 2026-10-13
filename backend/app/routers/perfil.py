# app/routers/perfil.py
# ─────────────────────────────────────────────────────────────────────────────
# CORRECCIONES vs versión anterior:
#
#  [PRF-1] get_perfil con role="admin": si el id no existía en la tabla
#          administrador, `row` era None y `row["role"] = "admin"` lanzaba
#          TypeError (NoneType). Se agrega verificación explícita.
#
#  [PRF-2] update_perfil: el cambio de contraseña se ejecutaba PRIMERO con su
#          propio UPDATE, y luego el bloque de campos (nombre/email/telefono)
#          hacía otro UPDATE separado. Si la segunda consulta fallaba, la
#          contraseña YA estaba cambiada en BD pero la respuesta era 500.
#          Se unifica todo en un solo UPDATE o se asegura orden correcto.
#
#  [PRF-3] update_perfil: si body.email era distinto al email actual, no se
#          verificaba si ese email ya pertenece a otro usuario → duplicados.
#
#  [PRF-4] update_perfil: el admin no tenía PUT de perfil. Si el token era
#          de admin y se llamaba a este endpoint, la query buscaba en `usuario`
#          por id_admin → no encontraba nada → 404 confuso.
#          Se diferencia por role igual que en GET.
#
#  [PRF-5] hora en citas del perfil: mismo problema timedelta que [ADM-3]/[CIT-7].
# ─────────────────────────────────────────────────────────────────────────────

import datetime as dt

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.security import get_current_user, hash_password, verify_password

router = APIRouter(prefix="/api/perfil", tags=["perfil"])


# ── Schemas ───────────────────────────────────────────────────────────────────

class UpdatePerfilBody(BaseModel):
    """Esquema para la actualización de datos del perfil de usuario o contraseña."""
    nombre:            Optional[str] = None
    email:             Optional[str] = None
    telefono:          Optional[str] = None
    contrasena_actual: Optional[str] = None
    contrasena_nueva:  Optional[str] = None


# ── Helper hora ───────────────────────────────────────────────────────────────

def _fmt_hora(value) -> str:
    """[PRF-5] timedelta → HH:MM."""
    if value is None:
        return ""
    if isinstance(value, dt.timedelta):
        total = int(value.total_seconds())
        h, rem = divmod(total, 3600)
        m, _   = divmod(rem, 60)
        return f"{h:02d}:{m:02d}"
    return str(value)


# ── GET /api/perfil ───────────────────────────────────────────────────────────

@router.get("")
def get_perfil(authorization: str = Header(None)):
    """Obtiene el perfil del usuario actual junto con sus vehículos asociados y citas recientes."""
    payload = get_current_user(authorization)
    uid  = payload["sub"]
    role = payload.get("role", "cliente")

    with get_db() as conn:
        cur = conn.cursor()

        if role == "admin":
            cur.execute(
                "SELECT id_admin AS id, nombre, apellido, email FROM administrador WHERE id_admin = %s",
                (uid,)
            )
            row = cur.fetchone()
            # [PRF-1] Verificación explícita antes de acceder al dict
            if not row:
                raise HTTPException(status_code=404, detail="Administrador no encontrado")
            return {
                "id":      row["id"],
                "nombre":  f"{row['nombre']} {row.get('apellido', '')}".strip(),
                "email":   row["email"],
                "role":    "admin",
            }

        # role == "cliente"
        cur.execute(
            "SELECT id_usuario AS id, nombre, username, email, telefono FROM usuario WHERE id_usuario = %s",
            (uid,)
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        row["role"] = "cliente"

        # Vehículos del usuario
        cur.execute(
            "SELECT id_vehiculo, marca, modelo, año, color, numero_de_placa FROM vehiculo WHERE id_usuario = %s",
            (uid,)
        )
        row["vehiculos"] = cur.fetchall()

        # Últimas 10 citas
        cur.execute("""
            SELECT c.id_cita AS id, s.nombre AS servicio,
                   c.fecha, c.hora, c.estado, c.monto
            FROM cita c
            LEFT JOIN servicio s ON c.id_servicio = s.id_servicio
            WHERE c.id_usuario = %s AND c.estado != 'cancelada'
            ORDER BY c.fecha DESC
            LIMIT 10
        """, (uid,))
        citas = cur.fetchall()
        for c in citas:
            if c.get("fecha"):
                c["fecha"] = str(c["fecha"])
            c["hora"] = _fmt_hora(c.get("hora"))   # [PRF-5]
        row["citas"] = citas

    return row


# ── PUT /api/perfil ───────────────────────────────────────────────────────────

@router.put("")
def update_perfil(body: UpdatePerfilBody, authorization: str = Header(None)):
    """Actualiza la información personal, email o contraseña del usuario autenticado."""
    payload = get_current_user(authorization)
    uid  = payload["sub"]
    role = payload.get("role", "cliente")

    with get_db() as conn:
        cur = conn.cursor()

        # [PRF-4] Diferenciar admin de cliente
        if role == "admin":
            cur.execute(
                "SELECT id_admin AS id, nombre, email FROM administrador WHERE id_admin = %s",
                (uid,)
            )
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Administrador no encontrado")

            fields, values = [], []
            if body.nombre: fields.append("nombre = %s"); values.append(body.nombre.strip())
            if body.email:
                # [PRF-3] Verificar email único (en administrador)
                cur.execute(
                    "SELECT id_admin FROM administrador WHERE email = %s AND id_admin != %s LIMIT 1",
                    (body.email.lower(), uid)
                )
                if cur.fetchone():
                    raise HTTPException(status_code=400, detail="Ese email ya está en uso")
                fields.append("email = %s")
                values.append(body.email.lower().strip())

            if fields:
                values.append(uid)
                cur.execute(f"UPDATE administrador SET {', '.join(fields)} WHERE id_admin = %s", values)
            return {"ok": True}

        # ── cliente ──────────────────────────────────────────────────────────
        cur.execute("SELECT * FROM usuario WHERE id_usuario = %s", (uid,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # [PRF-3] Verificar email único antes de cualquier update
        if body.email and body.email.lower().strip() != row["email"]:
            cur.execute(
                "SELECT id_usuario FROM usuario WHERE email = %s AND id_usuario != %s LIMIT 1",
                (body.email.lower().strip(), uid)
            )
            if cur.fetchone():
                raise HTTPException(status_code=400, detail="Ese email ya está en uso")

        # [PRF-2] Construir un solo UPDATE que incluya contraseña si aplica
        fields, values = [], []

        if body.nombre:   fields.append("nombre = %s");   values.append(body.nombre.strip())
        if body.email:    fields.append("email = %s");    values.append(body.email.lower().strip())
        if body.telefono: fields.append("telefono = %s"); values.append(body.telefono.strip())

        # Cambio de contraseña: validar primero, luego agregar al mismo UPDATE
        if body.contrasena_nueva:
            if not body.contrasena_actual:
                raise HTTPException(status_code=400, detail="Debes proporcionar tu contraseña actual")
            if not verify_password(body.contrasena_actual, row["contrasena"]):
                raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")
            if len(body.contrasena_nueva) < 6:
                raise HTTPException(status_code=400, detail="La nueva contraseña debe tener al menos 6 caracteres")
            fields.append("contrasena = %s")
            values.append(hash_password(body.contrasena_nueva))

        if fields:
            values.append(uid)
            cur.execute(
                f"UPDATE usuario SET {', '.join(fields)} WHERE id_usuario = %s",
                values
            )

    return {"ok": True}

# ── POST /api/perfil/vehiculos ────────────────────────────────────────────────

class VehiculoBody(BaseModel):
    numero_de_placa: str
    año: int
    marca: str
    modelo: str
    color: str

@router.post("/vehiculos")
def create_vehiculo(body: VehiculoBody, authorization: str = Header(None)):
    """Registra un nuevo vehículo en la cuenta del cliente autenticado."""
    payload = get_current_user(authorization)
    uid = payload["sub"]
    role = payload.get("role", "cliente")
    
    if role != "cliente":
        raise HTTPException(status_code=403, detail="Solo los clientes pueden registrar vehículos")
        
    with get_db() as conn:
        cur = conn.cursor()
        
        # Verificar si la placa ya existe
        cur.execute("SELECT id_vehiculo FROM vehiculo WHERE numero_de_placa = %s", (body.numero_de_placa.strip(),))
        if cur.fetchone():
            raise HTTPException(status_code=400, detail="Ya existe un vehículo con esa placa")
            
        cur.execute(
            """INSERT INTO vehiculo (id_usuario, numero_de_placa, año, marca, modelo, color) 
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (uid, body.numero_de_placa.strip().upper(), body.año, body.marca.strip(), body.modelo.strip(), body.color.strip())
        )
        conn.commit()
    return {"ok": True}
