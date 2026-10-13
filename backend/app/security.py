import os
import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException

SECRET_KEY  = os.getenv("DRIVEN_YIELD_SECRET") or os.getenv("driven yield_SECRET", "driven yield_dev_secret_CHANGE_IN_PROD_2026")
ALGORITHM   = "HS256"
TOKEN_HOURS = 72

def hash_password(plain: str) -> str:
    """Genera un hash seguro bcrypt para la contraseña en texto plano."""
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    """Verifica si una contraseña en texto plano coincide con el hash bcrypt almacenado."""
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except Exception:
        return False

def create_token(payload: dict) -> str:
    """Crea un JSON Web Token (JWT) firmado con vigencia configurada."""
    now  = datetime.now(timezone.utc)
    data = payload.copy()
    data["sub"] = str(data["sub"])
    data["iat"] = now
    data["exp"] = now + timedelta(hours=TOKEN_HOURS)
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    """Decodifica y valida un token JWT. Lanza HTTPException 401 si es inválido o expiró."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_sub": False})
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalido o expirado")

def get_current_user(authorization: str | None) -> dict:
    """Extrae y valida el usuario actual a partir del header de autorización Bearer."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No autenticado")
    token   = authorization.split(" ", 1)[1].strip()
    payload = decode_token(token)
    if "sub" not in payload or "role" not in payload:
        raise HTTPException(status_code=401, detail="Token malformado")
    payload["sub"] = int(payload["sub"])
    return payload

def require_admin(authorization: str | None) -> dict:
    """Verifica que el usuario autenticado cuente con el rol de administrador."""
    user = get_current_user(authorization)
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Acceso solo para administradores")
    return user
