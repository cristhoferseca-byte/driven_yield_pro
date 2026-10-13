import os
import pymysql
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

MYSQL_CONFIG = {
    "host":            os.getenv("DB_HOST", "localhost"),
    "port":            int(os.getenv("DB_PORT", "3306")),
    "user":            os.getenv("DB_USER", "root"),
    "password":        os.getenv("DB_PASSWORD", ""),
    "database":        os.getenv("DB_NAME", "driven_yield1"),
    "cursorclass":     pymysql.cursors.DictCursor
}

SUPABASE_URL = os.getenv("SUPABASE_URL", "")

def migrate():
    if not SUPABASE_URL:
        print("ERROR: SUPABASE_URL no está configurada en el archivo .env")
        return

    print("Conectando a MySQL local...")
    try:
        mysql_conn = pymysql.connect(**MYSQL_CONFIG)
        mysql_cur = mysql_conn.cursor()
    except Exception as e:
        print(f"Error conectando a MySQL: {e}")
        return

    print("Conectando a Supabase PostgreSQL...")
    try:
        pg_conn = psycopg2.connect(SUPABASE_URL)
        pg_conn.autocommit = True
        pg_cur = pg_conn.cursor()
    except Exception as e:
        print(f"Error conectando a Supabase: {e}")
        return

    # 1. Crear estructura de tablas en PostgreSQL
    print("Creando estructura de tablas en Supabase...")
    tables_sql = """
    DROP TABLE IF EXISTS carrito CASCADE;
    DROP TABLE IF EXISTS detalle_factura CASCADE;
    DROP TABLE IF EXISTS pedido CASCADE;
    DROP TABLE IF EXISTS producto CASCADE;
    DROP TABLE IF EXISTS historial_cita CASCADE;
    DROP TABLE IF EXISTS password_reset_tokens CASCADE;
    DROP TABLE IF EXISTS cita CASCADE;
    DROP TABLE IF EXISTS mecanico CASCADE;
    DROP TABLE IF EXISTS servicio CASCADE;
    DROP TABLE IF EXISTS vehiculo CASCADE;
    DROP TABLE IF EXISTS usuario CASCADE;
    DROP TABLE IF EXISTS administrador CASCADE;

    CREATE TABLE administrador (
        id_admin SERIAL PRIMARY KEY,
        nombre VARCHAR(100),
        apellido VARCHAR(100),
        email VARCHAR(150) UNIQUE,
        contrasena VARCHAR(255),
        token VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE usuario (
        id_usuario SERIAL PRIMARY KEY,
        nombre VARCHAR(150),
        username VARCHAR(50) UNIQUE,
        email VARCHAR(150) UNIQUE,
        telefono VARCHAR(50),
        contrasena VARCHAR(255),
        token VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE vehiculo (
        id_vehiculo SERIAL PRIMARY KEY,
        marca VARCHAR(100),
        modelo VARCHAR(100),
        año VARCHAR(10),
        color VARCHAR(50),
        numero_de_placa VARCHAR(50),
        id_usuario INT REFERENCES usuario(id_usuario) ON DELETE CASCADE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE servicio (
        id_servicio SERIAL PRIMARY KEY,
        nombre VARCHAR(150),
        categoria VARCHAR(100),
        precio DECIMAL(10,2),
        duracion VARCHAR(50),
        descripcion TEXT,
        imagen VARCHAR(255),
        activo INT DEFAULT 1
    );

    CREATE TABLE mecanico (
        id_mecanico SERIAL PRIMARY KEY,
        nombre VARCHAR(150),
        especialidad VARCHAR(150),
        telefono VARCHAR(50),
        disponible INT DEFAULT 1,
        activo INT DEFAULT 1
    );

    CREATE TABLE cita (
        id_cita SERIAL PRIMARY KEY,
        fecha DATE,
        hora TIME,
        notas TEXT,
        monto DECIMAL(10,2),
        estado VARCHAR(50) DEFAULT 'pendiente',
        id_usuario INT REFERENCES usuario(id_usuario) ON DELETE CASCADE,
        id_vehiculo INT REFERENCES vehiculo(id_vehiculo) ON DELETE CASCADE,
        id_servicio INT REFERENCES servicio(id_servicio),
        id_mecanico INT REFERENCES mecanico(id_mecanico),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE password_reset_tokens (
        id SERIAL PRIMARY KEY,
        id_usuario INT REFERENCES usuario(id_usuario) ON DELETE CASCADE,
        email VARCHAR(150),
        token VARCHAR(255) UNIQUE,
        expires_at TIMESTAMP
    );

    CREATE TABLE producto (
        id_producto SERIAL PRIMARY KEY,
        nombre VARCHAR(100),
        descripcion TEXT,
        precio DECIMAL(10,2) DEFAULT 0.00,
        stock INT DEFAULT 0,
        activo INT DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE pedido (
        id_pedido SERIAL PRIMARY KEY,
        id_usuario INT REFERENCES usuario(id_usuario) ON DELETE CASCADE,
        total DECIMAL(10,2) DEFAULT 0.00,
        estado VARCHAR(50) DEFAULT 'pendiente',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE detalle_factura (
        id_detalle SERIAL PRIMARY KEY,
        id_pedido INT REFERENCES pedido(id_pedido) ON DELETE CASCADE,
        id_producto INT REFERENCES producto(id_producto) ON DELETE CASCADE,
        cantidad INT DEFAULT 1,
        precio_unit DECIMAL(10,2) DEFAULT 0.00
    );

    CREATE TABLE carrito (
        id_carrito SERIAL PRIMARY KEY,
        id_usuario INT REFERENCES usuario(id_usuario) ON DELETE CASCADE,
        id_producto INT REFERENCES producto(id_producto) ON DELETE CASCADE,
        cantidad INT DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE historial_cita (
        id_historial SERIAL PRIMARY KEY,
        id_cita INT REFERENCES cita(id_cita) ON DELETE CASCADE,
        estado_anterior VARCHAR(50),
        estado_nuevo VARCHAR(50),
        cambiado_por INT,
        fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    try:
        pg_cur.execute(tables_sql)
        print("Tablas creadas correctamente.")
    except Exception as e:
        print(f"Error creando tablas: {e}")
        return

    # 2. Migrar Datos
    tablas_a_migrar = [
        "administrador", "usuario", "servicio", "mecanico", "vehiculo", "cita", "historial_cita", "password_reset_tokens",
        "producto", "pedido", "detalle_factura", "carrito"
    ]

    for tabla in tablas_a_migrar:
        print(f"Migrando datos de la tabla '{tabla}'...")
        try:
            mysql_cur.execute(f"SELECT * FROM {tabla}")
            filas = mysql_cur.fetchall()
            
            if not filas:
                print(f"  -> Tabla '{tabla}' está vacía. Saltando.")
                continue

            columnas = filas[0].keys()
            cols_str = ", ".join(columnas)
            placeholders = ", ".join(["%s"] * len(columnas))
            
            insert_query = f"INSERT INTO {tabla} ({cols_str}) VALUES ({placeholders}) ON CONFLICT DO NOTHING;"
            
            datos_insertar = []
            for fila in filas:
                datos_insertar.append(tuple(fila[col] for col in columnas))
            
            psycopg2.extras.execute_batch(pg_cur, insert_query, datos_insertar)
            
            # Sincronizar secuencias
            if f"id_{tabla}" in columnas:
                pg_cur.execute(f"SELECT setval(pg_get_serial_sequence('{tabla}', 'id_{tabla}'), COALESCE(MAX(id_{tabla}), 1)) FROM {tabla};")
            elif tabla == "password_reset_tokens":
                pg_cur.execute(f"SELECT setval(pg_get_serial_sequence('{tabla}', 'id'), COALESCE(MAX(id), 1)) FROM {tabla};")
                
            print(f"  -> {len(filas)} filas migradas exitosamente.")
        except Exception as e:
            print(f"  -> ERROR al migrar tabla '{tabla}': {e}")

    print("\n¡Migración a Supabase completada con éxito!")
    mysql_conn.close()
    pg_conn.close()

if __name__ == "__main__":
    migrate()
