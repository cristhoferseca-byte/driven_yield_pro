const BASE_URL = 'http://localhost:8000/api';

async function makeRequest(method, endpoint, data = null) {
    const url = `${BASE_URL}${endpoint}`;
    const options = { method, headers: {} };
    
    if (data) {
        options.headers['Content-Type'] = 'application/json';
        options.body = JSON.stringify(data);
    }

    try {
        const res = await fetch(url, options);
        let body = await res.text();
        console.log(`[${method}] ${url}`);
        console.log(`Status: ${res.status}`);
        console.log(`Response: ${body.substring(0, 200)}${body.length > 200 ? '...' : ''}`);
        console.log('-'.repeat(50));
    } catch (e) {
        console.log(`[${method}] ${url}`);
        console.log(`Error de conexión: El servidor backend puede estar apagado.`);
        console.log('-'.repeat(50));
    }
}

async function runTests() {
    console.log("Iniciando Pruebas de API...\n" + "=".repeat(50));

    // 1. GET: Petición exitosa (debería devolver 200)
    await makeRequest("GET", "/servicios");

    // 2. POST (Error Forzado 401): Credenciales inválidas
    await makeRequest("POST", "/auth/login", { username: "usuario_falso", contrasena: "clave_falsa" });

    // 3. PUT (Error Forzado 401/404): Modificar cita sin autorización ni token
    await makeRequest("PUT", "/citas/999", { estado: "cancelada" });

    // 4. DELETE (Error Forzado 401/404): Eliminar cita sin autorización
    await makeRequest("DELETE", "/citas/999");

    // 5. PATCH (Error Forzado 405): Método no permitido (FastAPI rechazará porque no existe el endpoint PATCH)
    await makeRequest("PATCH", "/servicios");

    console.log("Pruebas finalizadas.");
}

runTests();
