# driven yield Pro — Backend v2.0

## Estructura

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app, CORS, middleware
│   ├── database.py       # Conexión a PostgreSQL (Supabase / psycopg2)
│   ├── security.py       # JWT + bcrypt + dependencias de auth
│   ├── email_service.py  # Envío SMTP y plantillas de correo
│   └── routers/
│       ├── auth.py       # /api/auth/*
│       ├── admin.py      # /api/admin/*
│       ├── citas.py      # /api/citas/*
│       ├── servicios.py  # /api/servicios
│       ├── perfil.py     # /api/perfil
│       ├── mecanicos.py  # /api/mecanicos
│       └── practica.py   # /api/practica-guiada (ejercicios)
├── run.py
└── requirements.txt
```

## Instalación

```bash
pip install -r requirements.txt
python run.py
# o: uvicorn app.main:app --reload --port 8000
```

## Variables de entorno (opcionales)

| Variable             | Descripción                          | Default                              |
|----------------------|--------------------------------------|--------------------------------------|
| `DRIVEN_YIELD_SECRET`| Clave JWT (¡cambiar en producción!)  | `driven yield_dev_secret_CHANGE_IN_PROD_2026` |
| `SUPABASE_URL`       | Cadena de conexión PostgreSQL        | *(Requerida para Supabase/PostgreSQL)* |
| `BASE_URL`           | URL base del frontend (correos)      | `http://localhost:5173`              |
| `CORS_ORIGINS`       | Orígenes CORS separados por coma     | `http://localhost:5173,http://localhost:3000` |
| `MAIL_HOST`          | Servidor SMTP                        | `smtp.gmail.com`                     |
| `MAIL_PORT`          | Puerto SMTP                          | `587`                                |
| `MAIL_USER`          | Email remitente                      | *(vacío = DRY-RUN, imprime en consola)* |
| `MAIL_PASSWORD`      | Contraseña / app-key SMTP            | *(vacío)*                            |
| `MAIL_FROM`          | Dirección From                       | igual a `MAIL_USER`                  |

## SQL adicional requerido

La tabla `password_reset_tokens` debe existir para el flujo forgot-password:

```sql
CREATE TABLE IF NOT EXISTS password_reset_tokens (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  id_usuario  INT          NOT NULL,
  token       VARCHAR(128) NOT NULL UNIQUE,
  expires_at  DATETIME     NOT NULL,
  used        TINYINT(1)   DEFAULT 0,
  FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE
);
```

## Migración de contraseñas (SHA-256 → bcrypt)

El backend anterior guardaba contraseñas con `hashlib.sha256` (sin sal).
El nuevo backend usa **bcrypt** exclusivamente.

Después de reemplazar el backend, los usuarios con contraseñas antiguas
no podrán hacer login hasta que sus hashes sean migrados.

**Opción A — Migración en caliente (recomendada):**
Al hacer login, detectar si el hash empieza con `$2b$` (bcrypt) o no.
Si no es bcrypt, comparar con SHA-256, y si coincide, re-hashear con bcrypt
y guardar. Solo durante el periodo de transición.

**Opción B — Reset masivo:**
Enviar correo a todos los usuarios para que restablezcan su contraseña
via el nuevo endpoint `POST /api/auth/forgot-password`.

**Script de migración manual (ejecutar UNA SOLA VEZ):**
```sql
-- Marcar contraseñas antiguas (SHA-256 tiene exactamente 64 hex chars)
-- No hace nada automáticamente; el script Python las migra al primer login.
SELECT id_usuario, username, LENGTH(contrasena) AS len
FROM usuario
WHERE contrasena NOT LIKE '$2b$%';
```

---

## Errores corregidos

### `security.py`
| Código | Problema original | Corrección |
|--------|-------------------|------------|
| HASH-1 | `hashlib.sha256` sin sal — vulnerable a rainbow tables | Reemplazado por **bcrypt** (passlib) |
| HASH-2 | `plain == stored` aceptaba contraseñas en texto plano | Eliminado |
| HASH-3 | Tres estrategias de verificación mezcladas | Una sola: bcrypt |
| JWT-1  | `datetime.utcnow()` deprecado en Python 3.12+ | `datetime.now(timezone.utc)` |
| JWT-2  | Sin claim `iat` (issued-at) en el token | Agregado |
| SEC-1  | `SECRET_KEY` hardcodeada en código fuente | Lee de variable de entorno `driven yield_SECRET` |
| SEC-2  | `get_current_user` / `require_admin` usaban `Header(None)` como param normal | Convertidas a funciones puras que reciben el string directamente |

### `routers/auth.py`
| Código | Problema original | Corrección |
|--------|-------------------|------------|
| AUTH-1 | Conexión cerrada antes de leer `lastrowid` en register | Todo dentro del mismo `with get_db()` |
| AUTH-2 | Conexión cerrada antes de `verify_password` en login | Mismo bloque |
| AUTH-3 | `EmailStr` importado sin usar | Eliminado |
| AUTH-4 | `/me` con role admin sin verificar existencia | Verificación explícita con 404 |
| AUTH-5 | No existía `forgot-password` | Agregado con token seguro + correo |
| AUTH-6 | No existía `reset-password` | Agregado |

### `routers/admin.py`
| Código | Problema original | Corrección |
|--------|-------------------|------------|
| ADM-1  | Mismo patrón frágil conexión/verify_password | Unificado |
| ADM-2  | `delete_cita`: historial borrado antes de verificar existencia de cita | Verificación primero |
| ADM-3  | `hora` devuelta como `timedelta` → error JSON | Formateada como `HH:MM` |
| ADM-4  | `require_admin` llamado incorrectamente | Llamada corregida |
| ADM-5  | Sin endpoint de estadísticas | Agregado `GET /api/admin/stats` |

### `routers/citas.py`
| Código | Problema original | Corrección |
|--------|-------------------|------------|
| CIT-1  | `marca` podía quedar vacía si vehiculo="" y marca="" | Fallback a "Desconocido" |
| CIT-2  | Sin placa → múltiples vehículos "SIN-PLACA" por usuario | Búsqueda por marca+modelo antes de crear |
| CIT-3  | Servicio inexistente → silenciosamente usa `id=1` | Lanza HTTP 400 |
| CIT-4  | Sin mecánico → usa `id=1` hardcodeado → posible FK violation | Usa `NULL` |
| CIT-5  | Cliente podía poner estado "completada"/"confirmada" | Solo admin puede poner esos estados |
| CIT-6  | Historial borrado antes de verificar propiedad de la cita | Verificación primero |
| CIT-7  | `hora` como `timedelta` → error JSON | Formateada como `HH:MM` |
| CIT-8  | Sin notificación al crear cita | Correo enviado tras crear |

### `routers/perfil.py`
| Código | Problema original | Corrección |
|--------|-------------------|------------|
| PRF-1  | `row["role"]` sobre `None` si admin no existía → TypeError | Verificación explícita |
| PRF-2  | Contraseña y campos actualizados en dos queries separadas — inconsistente | Un solo UPDATE |
| PRF-3  | Nuevo email no verificado contra duplicados | Verificación de unicidad antes de UPDATE |
| PRF-4  | Admin intentando actualizar perfil buscaba en tabla `usuario` | Diferenciado por role |
| PRF-5  | `hora` como `timedelta` en citas del perfil | Formateada como `HH:MM` |

### `routers/servicios.py`
| Sin código | `precio` (Decimal) podía fallar serialización JSON | Cast a `float` |
| Sin código | `duracion` como `timedelta` podía dar error | Formateada como `HH:MM` |
