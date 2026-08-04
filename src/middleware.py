import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from pythonjsonlogger import jsonlogger

# Configuración del Logger JSON
logger = logging.getLogger("ops_fitness")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Filtrar el ruido de Kubernetes (Prometheus y Liveness Probes)
        if request.url.path in ["/healthz", "/metrics"]:
            return await call_next(request)

        start_time = time.time()
        response = await call_next(request)
        duration_ms = round((time.time() - start_time) * 1000, 2)

        # 2. Contexto base de la petición
        log_context = {
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
            "client_ip": request.client.host if request.client else "unknown"
        }

        # 3. Lógica de Negocio: Detectar creación de workout
        if request.url.path == "/api/v1/workouts" and request.method == "POST":
            workout_type = request.query_params.get("workout_type", "unknown")
            log_context["workout_type"] = workout_type
            
            if response.status_code == 201:
                log_context["event"] = "workout_created"
                logger.info("Workout registrado exitosamente", extra=log_context)
            else:
                log_context["event"] = "workout_failed"
                logger.error("Error al registrar workout", extra=log_context)
        else:
            # 4. Peticiones HTTP genéricas
            log_context["event"] = "http_request"
            if response.status_code >= 400:
                logger.warning("Petición HTTP fallida", extra=log_context)
            else:
                logger.info("Petición HTTP procesada", extra=log_context)

        return response