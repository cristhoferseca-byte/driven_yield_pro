"""
Script de utilidad para comprobar la existencia de un administrador en la BD
y crear uno por defecto o resetear credenciales de acceso inicial.
"""
import pymysql
import os
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "driven_yield1",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit": True,
}

try:
    conn = pymysql.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    # Check if admin exists
    cur.execute("SELECT id_admin, email FROM administrador;")
    admins = cur.fetchall()
    
    if len(admins) == 0:
        print("No admins found. Creating default admin.")
        email = "admin@drivenyield.com"
        password = "admin"
        hashed = hash_password(password)
        cur.execute(
            "INSERT INTO administrador (nombre, apellido, email, contrasena) VALUES (%s, %s, %s, %s)",
            ("Admin", "Principal", email, hashed)
        )
        print(f"Created Admin -> Email: {email} | Password: {password}")
    else:
        # Reset password for the first admin
        admin = admins[0]
        email = admin["email"]
        password = "admin"
        hashed = hash_password(password)
        cur.execute(
            "UPDATE administrador SET contrasena = %s WHERE id_admin = %s",
            (hashed, admin["id_admin"])
        )
        print(f"Existing Admin found. Password reset!")
        print(f"Email: {email} | Password: {password}")
    
    conn.close()
except Exception as e:
    print(f"Error: {e}")
