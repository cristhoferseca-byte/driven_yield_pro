# rehash_passwords.py
# ─────────────────────────────────────────────────────────────────────────────
# Detecta contraseñas en la tabla `usuario` que NO son hashes bcrypt válidos
# (texto plano, sha256, etc.) y las reemplaza con un hash bcrypt nuevo.
#
# A todos los usuarios afectados se les asigna la MISMA contraseña temporal
# (ver NUEVA_CONTRASENA abajo). Después pueden cambiarla con /forgot-password
# o tú les avisas cuál es.
#
# Requisitos: pip install bcrypt pymysql --break-system-packages
#
# Uso:
#   python rehash_passwords.py
# ─────────────────────────────────────────────────────────────────────────────

import bcrypt
import pymysql
import pymysql.cursors

# ── Configuración (ajusta si tu XAMPP usa otros datos) ──────────────────────
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "driven_yield1",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
}

# Contraseña temporal que se asignará a todos los usuarios con hash inválido
NUEVA_CONTRASENA = "Temporal123"


def es_bcrypt_valido(valor: str) -> bool:
    return isinstance(valor, str) and valor.startswith(("$2a$", "$2b$", "$2y$"))


def main():
    nuevo_hash = bcrypt.hashpw(NUEVA_CONTRASENA.encode(), bcrypt.gensalt()).decode()

    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id_usuario, username, contrasena FROM usuario")
            usuarios = cur.fetchall()

            afectados = [u for u in usuarios if not es_bcrypt_valido(u["contrasena"])]

            if not afectados:
                print("✅ Todos los usuarios ya tienen hash bcrypt válido. Nada que hacer.")
                return

            print(f"Usuarios con hash inválido detectados: {len(afectados)}")
            for u in afectados:
                cur.execute(
                    "UPDATE usuario SET contrasena = %s WHERE id_usuario = %s",
                    (nuevo_hash, u["id_usuario"])
                )
                print(f"  - {u['username']:<15} -> contraseña reseteada a '{NUEVA_CONTRASENA}'")

        conn.commit()
        print("\n✅ Listo. Esos usuarios ya pueden iniciar sesión con la contraseña temporal.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
