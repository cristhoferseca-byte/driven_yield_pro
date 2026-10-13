import logging
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
<<<<<<< HEAD
load_dotenv()

from app.routers import auth, admin, citas, servicios, perfil, practica, mecanicos
=======

# Cargar variables antes de importar routers
load_dotenv()

from app.routers import auth, admin, citas, servicios, perfil, practica, mecanicos, notificaciones
>>>>>>> origin/main

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,https://localhost:5173,http://localhost:3000").split(",")

app = FastAPI(
    title="driven yield Pro API",
    version="2.0.0",
    description="Backend para driven yield Pro System",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://localhost:5173",
        "http://127.0.0.1:5173",
        "https://127.0.0.1:5173",
        "http://localhost:3000",
        "https://localhost:3000",
        "null"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("%s %s", request.method, request.url.path)
    response = await call_next(request)
    return response

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(citas.router)
app.include_router(servicios.router)
app.include_router(perfil.router)
app.include_router(practica.router)
app.include_router(mecanicos.router)
app.include_router(notificaciones.router)

@app.get("/", tags=["Health"])
def root():
    """Endpoint raíz que retorna la versión actual de la API."""
    return {"status": "ok", "api": "driven yield Pro v2.0"}

@app.get("/health", tags=["Health"])
def health():
    """Verifica el estado del servicio y la conectividad con la base de datos."""
    from app.database import get_db
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
        return {"status": "ok", "db": "connected"}
    except Exception as exc:
        return {"status": "error", "db": str(exc)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)