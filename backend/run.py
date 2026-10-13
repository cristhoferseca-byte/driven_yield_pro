"""
Punto de entrada para ejecutar el servidor backend FastAPI de Driven Yield Pro.
Carga las variables de entorno y levanta el servidor uvicorn en modo reload.
"""
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env', override=True)

import uvicorn
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.join(BASE_DIR, "..", "certs", "localhost.key")
cert_path = os.path.join(BASE_DIR, "..", "certs", "localhost.crt")

use_ssl = os.path.exists(key_path) and os.path.exists(cert_path)

if __name__ == "__main__":
    run_kwargs = {
        "app": "app.main:app",
        "host": "0.0.0.0",
        "port": 8000,
        "reload": True,
    }
    if use_ssl:
        run_kwargs["ssl_keyfile"] = key_path
        run_kwargs["ssl_certfile"] = cert_path
    
    uvicorn.run(**run_kwargs)
