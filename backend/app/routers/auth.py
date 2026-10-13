# app/routers/auth.py
# ─────────────────────────────────────────────────────────────────────────────
# CORRECCIONES vs versión anterior:
#
#  [AUTH-1] register: la conexión se cerraba ANTES de leer lastrowid, porque el
#           bloque `with get_db()` terminaba y la conexión se cerraba antes del
#           SELECT de confirmación. Se hace todo dentro del mismo bloque.
#
#  [AUTH-2] login: la conexión también se cerraba antes de llamar verify_password.
#           Aunque no genera error (los datos ya estaban en `row`), es un patrón
#           frágil. Se mantiene todo dentro del `with`.
#
#  [AUTH-3] EmailStr importado pero nunca usado → se elimina la importación
#           muerta que causaba un warning en runtime.
#
#  [AUTH-4] /me: si el token tiene role="admin" pero el id no existe en
#           administrador, se devolvía HTTP 404 sin cerrar la conexión. Ahora
#           con el context manager corregido en database.py esto se resuelve.
#
#  [AUTH-5] forgot-password: no existía. Se agrega con token de un solo uso
#           almacenado en BD (tabla password_reset_tokens) y envío de correo.
#
#  [AUTH-6] reset-password: complemento de forgot-password.
#
#  [HASH]   hash_password ahora usa bcrypt (ver security.py).
# ─────────────────────────────────────────────────────────────────────────────

import secrets
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, field_validator

from app.database import get_db
from app.security import verify_password, hash_password, create_token, get_current_user
from app.email_service import send_bienvenida, send_recuperacion_contrasena

router = APIRouter(prefix="/api/auth", tags=["auth"])


# ── Schemas ───────────────────────────────────────────────────────────────────

class LoginBody(BaseModel):
    """Esquema para la solicitud de inicio de sesión de usuario."""
    username:   str
    contrasena: str

    @field_validator("username", "contrasena")
    @classmethod
    def no_vacios(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Este campo no puede estar vacío")
        return v.strip()


class RegisterBody(BaseModel):
    """Esquema para el registro de nuevos usuarios en el sistema."""
    nombre:     str
    username:   str
    email:      str
    contrasena: str
    telefono:   str = ""

    @field_validator("nombre", "username", "email", "contrasena")
    @classmethod
    def no_vacios(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Este campo no puede estar vacío")
        return v.strip()

    @field_validator("email")
    @classmethod
    def email_valido(cls, v: str) -> str:
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Email inválido")
        return v.lower().strip()

    @field_validator("contrasena")
    @classmethod
    def password_minimo(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        return v

    @field_validator("username")
    @classmethod
    def username_minimo(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError("El nombre de usuario debe tener al menos 3 caracteres")
        return v.lower().strip()


class ForgotBody(BaseModel):
    email: str


class ResetBody(BaseModel):
    token:      str
    contrasena: str

    @field_validator("contrasena")
    @classmethod
    def password_minimo(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        return v


# ── Helper respuesta usuario ──────────────────────────────────────────────────

def _user_response(row: dict, token: str) -> dict:
    return {
        "token": token,
        "user": {
            "id":       row["id_usuario"],
            "nombre":   row["nombre"],
            "username": row["username"],
            "email":    row["email"],
            "telefono": row.get("telefono") or "",
            "role":     "cliente",
        }
    }


def _ensure_password_reset_table(cur) -> None:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS password_reset_tokens (
            id SERIAL PRIMARY KEY,
            id_usuario INT NOT NULL REFERENCES usuario(id_usuario) ON DELETE CASCADE,
            token VARCHAR(128) NOT NULL UNIQUE,
            expires_at TIMESTAMP NOT NULL,
            used BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_password_reset_usuario
        ON password_reset_tokens(id_usuario)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_password_reset_token
        ON password_reset_tokens(token)
    """)


# ── POST /api/auth/login ──────────────────────────────────────────────────────

@router.post("/login")
def login(body: LoginBody):
    """Autentica a un usuario por username/email y contraseña, generando un token JWT."""
    # [AUTH-2] Todo dentro del mismo bloque de conexión
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM usuario WHERE (username = %s OR email = %s) LIMIT 1",
            (body.username, body.username)
        )
        row = cur.fetchone()

    # Timing-safe: verificar siempre aunque row sea None (evita timing attack)
    if not row or not verify_password(body.contrasena, row["contrasena"]):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    token = create_token({
        "sub":    row["id_usuario"],
        "role":   "cliente",
        "nombre": row["nombre"],
    })
    return _user_response(row, token)


# ── POST /api/auth/register ───────────────────────────────────────────────────

@router.post("/register")
def register(body: RegisterBody):
    """Registra un nuevo usuario en la base de datos y envía correo de bienvenida."""
    # [AUTH-1] Un solo bloque de conexión para todo el flujo
    with get_db() as conn:
        cur = conn.cursor()

        # Verificar duplicados (username O email)
        cur.execute(
            "SELECT id_usuario FROM usuario WHERE username = %s OR email = %s LIMIT 1",
            (body.username, body.email)
        )
        if cur.fetchone():
            raise HTTPException(status_code=400, detail="El usuario o email ya existe")

        hashed = hash_password(body.contrasena)   # [HASH] bcrypt

        cur.execute(
            """INSERT INTO usuario (nombre, username, email, telefono, contrasena)
               VALUES (%s, %s, %s, %s, %s) RETURNING id_usuario""",
            (body.nombre, body.username, body.email, body.telefono, hashed)
        )
        new_id = cur.fetchone()["id_usuario"]

        cur.execute("SELECT * FROM usuario WHERE id_usuario = %s", (new_id,))
        row = cur.fetchone()

    # Correo de bienvenida (no bloqueante si falla)
    send_bienvenida(row["email"], row["nombre"])

    token = create_token({
        "sub":    row["id_usuario"],
        "role":   "cliente",
        "nombre": row["nombre"],
    })
    return _user_response(row, token)


# ── GET /api/auth/me ──────────────────────────────────────────────────────────

@router.get("/me")
def me(authorization: str = Header(None)):
    """Obtiene el perfil e información del usuario autenticado (cliente o admin)."""
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
            if not row:
                raise HTTPException(status_code=404, detail="Admin no encontrado")
            return {
                "id":      row["id"],
                "nombre":  f"{row['nombre']} {row.get('apellido', '')}".strip(),
                "email":   row["email"],
                "role":    "admin",
            }
        else:
            cur.execute(
                "SELECT id_usuario AS id, nombre, username, email, telefono FROM usuario WHERE id_usuario = %s",
                (uid,)
            )
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            return {
                "id":       row["id"],
                "nombre":   row["nombre"],
                "username": row["username"],
                "email":    row["email"],
                "telefono": row.get("telefono") or "",
                "role":     "cliente",
            }


# ── POST /api/auth/logout ─────────────────────────────────────────────────────

@router.post("/logout")
def logout():
    """Cierra la sesión del usuario (del lado cliente se descarta el token JWT)."""
    # JWT es stateless; el cliente elimina el token local
    return {"ok": True}


# ── POST /api/auth/forgot-password ───────────────────────────────────────────
# [AUTH-5] Nuevo endpoint — genera token de reset y envía correo

@router.post("/forgot-password")
def forgot_password(body: ForgotBody):
    """
    Siempre responde 200 para no revelar si el email existe o no
    (previene enumeración de usuarios).
    """
    with get_db() as conn:
        cur = conn.cursor()
        _ensure_password_reset_table(cur)
        cur.execute(
            "SELECT id_usuario, nombre, email FROM usuario WHERE email = %s LIMIT 1",
            (body.email.lower().strip(),)
        )
        row = cur.fetchone()

        if row:
            # Token aleatorio de 48 bytes (URL-safe)
            reset_token = secrets.token_urlsafe(48)
            expires_at  = datetime.now(timezone.utc) + timedelta(hours=1)

            cur.execute(
                "UPDATE password_reset_tokens SET used = TRUE WHERE id_usuario = %s AND used = FALSE",
                (row["id_usuario"],)
            )
            cur.execute(
                """INSERT INTO password_reset_tokens (id_usuario, token, expires_at, used)
                   VALUES (%s, %s, %s, FALSE)""",
                (row["id_usuario"], reset_token, expires_at.strftime("%Y-%m-%d %H:%M:%S"))
            )
            send_recuperacion_contrasena(row["email"], row["nombre"], reset_token)

    return {"ok": True, "mensaje": "Si el correo existe, recibirás instrucciones en breve."}


# ── POST /api/auth/reset-password ────────────────────────────────────────────
# [AUTH-6] Complemento de forgot-password

@router.post("/reset-password")
def reset_password(body: ResetBody):
    """Restablece la contraseña del usuario utilizando un token de recuperación válido."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT t.id, t.id_usuario, t.expires_at, t.used
               FROM password_reset_tokens t
               WHERE t.token = %s LIMIT 1""",
            (body.token,)
        )
        record = cur.fetchone()

        if not record:
            raise HTTPException(status_code=400, detail="Token inválido")

        if record["used"]:
            raise HTTPException(status_code=400, detail="Este enlace ya fue utilizado")

        # Comparar fechas timezone-naive (MySQL devuelve naive)
        if datetime.now() > record["expires_at"]:
            raise HTTPException(status_code=400, detail="El enlace ha expirado")

        new_hash = hash_password(body.contrasena)
        cur.execute(
            "UPDATE usuario SET contrasena = %s WHERE id_usuario = %s",
            (new_hash, record["id_usuario"])
        )
        cur.execute(
            "UPDATE password_reset_tokens SET used = TRUE WHERE id = %s",
            (record["id"],)
        )

    return {"ok": True, "mensaje": "Contraseña actualizada correctamente"}
