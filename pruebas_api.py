import urllib.request
import urllib.error
import json

BASE_URL = "http://localhost:8000/api"

def print_result(method, url, status, response):
    print(f"[{method}] {url}")
    print(f"Status: {status}")
    print(f"Response: {response}")
    print("-" * 50)

def make_request(method, endpoint, data=None):
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url, method=method)
    if data:
        req.add_header("Content-Type", "application/json")
        json_data = json.dumps(data).encode("utf-8")
        req.data = json_data

    try:
        with urllib.request.urlopen(req) as response:
            body = response.read().decode("utf-8")
            print_result(method, url, response.status, body[:200] + "..." if len(body) > 200 else body)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print_result(method, url, e.code, body)
    except urllib.error.URLError as e:
        print_result(method, url, "ERROR", str(e.reason))

if __name__ == "__main__":
    print("Iniciando Pruebas de API...\n" + "="*50)

    # 1. GET: Petición exitosa
    make_request("GET", "/servicios")

    # 2. POST (Error Forzado 401): Credenciales inválidas
    make_request("POST", "/auth/login", {"username": "usuario_falso", "contrasena": "clave_falsa"})

    # 3. PUT (Error Forzado 401/404): Modificar sin autorización
    make_request("PUT", "/citas/999", {"estado": "cancelada"})

    # 4. DELETE (Error Forzado 401/404): Eliminar sin autorización
    make_request("DELETE", "/citas/999")

    # 5. PATCH (Error Forzado 405): Método no permitido (no existe en la API)
    make_request("PATCH", "/servicios")

    print("Pruebas finalizadas.")

# Pruebas de diagnostico y validacion de endpoints (Duvan)

# Validacion de formato de respuestas JSON y codigos de estado

