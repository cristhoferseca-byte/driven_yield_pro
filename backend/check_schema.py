import os
import pymysql

DB_CONFIG = {
    "host":            "localhost",
    "port":            3306,
    "user":            "root",
    "password":        "",
    "database":        "driven_yield1",
    "cursorclass":     pymysql.cursors.DictCursor
}

def get_schema():
    conn = pymysql.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    tablas = ["producto", "pedido", "detalle_factura", "carrito"]
    for t in tablas:
        try:
            cur.execute(f"DESCRIBE {t}")
            res = cur.fetchall()
            print(f"--- {t} ---")
            for r in res:
                print(r)
        except Exception as e:
            print(f"Error en {t}: {e}")

if __name__ == "__main__":
    get_schema()
