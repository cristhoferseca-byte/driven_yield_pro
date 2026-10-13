# app/database.py
# ─────────────────────────────────────────────────────────────────────────────
# Conexión a PostgreSQL (Supabase) con psycopg (v3).
# Migrado desde psycopg2-binary porque no hay wheel precompilado para
# versiones recientes de Python, y compilarlo desde fuente requiere pg_config
# (PostgreSQL instalado localmente). psycopg v3 sí trae wheels binarios.
# ─────────────────────────────────────────────────────────────────────────────
import os
import psycopg
from psycopg.rows import dict_row
from contextlib import contextmanager

SUPABASE_URL = os.getenv("SUPABASE_URL", "")

def get_connection():
    """
    Crea y retorna una conexión activa a la base de datos PostgreSQL en Supabase.
    """
    url = os.getenv("SUPABASE_URL", "")
    if not url:
        raise ValueError("La variable SUPABASE_URL no está configurada.")
    
    conn = psycopg.connect(url, row_factory=dict_row, autocommit=True)
    return conn


@contextmanager
def get_db():
    """
    Context manager que garantiza cierre de conexión.
    Si ocurre una excepción dentro del bloque `with get_db() as conn:`
    el error se propaga normalmente (FastAPI lo captura y responde 500).
    """
    conn = get_connection()
    try:
        yield conn
    except Exception:
        # Deja que la excepción suba; FastAPI genera HTTP 500 automáticamente.
        raise
    finally:
        conn.close()
