"""
Script para actualización y siembra del catálogo de servicios premium en la base de datos.
Permite insertar servicios que no existan previamente sin alterar los existentes.
"""
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_NAME = os.getenv("DB_NAME", "taller_db")

connection = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    cursorclass=pymysql.cursors.DictCursor
)

nuevos_servicios = [
    ("Mantenimiento Preventivo PRO", "Mantenimiento", 250000, "45 min", "Aceite sintético y filtros OEM"),
    ("Diagnóstico Computarizado Avanzado", "Diagnóstico", 150000, "60 min", "Escáner OBD2 y diagnóstico de sensores"),
    ("Actualización a Frenos Cerámicos", "Frenos", 450000, "150 min", "Frenos de alto desempeño y rectificado"),
    ("Sincronización Electrónica", "Mantenimiento", 350000, "180 min", "Bujías iridio y limpieza inyectores"),
    ("Alineación y Balanceo Láser 3D", "Llantas", 150000, "60 min", "Alineación láser 3D de 4 ruedas"),
    ("Mantenimiento Transmisión Automática", "Mantenimiento", 600000, "240 min", "Diálisis completa y fluido ATF"),
    ("Detailing y Recubrimiento Cerámico", "Estética", 1200000, "2880 min", "Corrección y protección cerámica 9H"),
    ("Restauración de Suspensión Deportiva", "Suspensión", 850000, "300 min", "Amortiguadores y bujes nuevos")
]

try:
    with connection.cursor() as cursor:
        for nombre, cat, precio, duracion, desc in nuevos_servicios:
            # Check if it exists
            cursor.execute("SELECT id_servicio FROM servicio WHERE nombre = %s", (nombre,))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO servicio (nombre, categoria, precio, duracion, descripcion, activo)
                    VALUES (%s, %s, %s, %s, %s, 1)
                """, (nombre, cat, precio, duracion, desc))
        connection.commit()
        print("Servicios premium actualizados correctamente.")
finally:
    connection.close()
