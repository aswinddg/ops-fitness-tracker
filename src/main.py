import time
from fastapi import FastAPI, Response, status
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from src.middleware import StructuredLoggingMiddleware

app = FastAPI(
    title="Ops Fitness Core API",
    description="API for the Ops Fitness Core",
    version="1..0",
    contact={
        "name": "Ops Fitness",
        "url": "https://www.ops-fitness.com",
        "email": "support@ops-fitness.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Metricas de negocio y sistema

WORKOUT_COUNTER = Counter(
    "fitness_workouts_total",
    "Total de sesiones de entrenamiento registradas",
    ["workout_type"],
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'Latencia de las peticiones HTTP en segundos',
    ['endpoint'],
)

@app.middleware("http")
async def measure_request_latency(request, call_next):
    """Mide la duración de cada petición HTTP por endpoint."""
    start_time = time.perf_counter()

    response = await call_next(request)

    elapsed_time = time.perf_counter() - start_time
    REQUEST_LATENCY.labels(endpoint=request.url.path).observe(elapsed_time)

    return response

# ✅ Registrar el middleware de logging estructurado DESPUÉS de métricas
app.add_middleware(StructuredLoggingMiddleware)

@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {
        "system": "Ops Fitness Tracker",
        "status": "online",
        "environment": "production"
    }

@app.get("/healthz", status_code=status.HTTP_200_OK)
def health_check():
    """Liveliness probe para orquestadores como EKS"""
    return {
        "status": "healthy",
        "service": "ops-fitness-core"    
    }

@app.get("/metrics")
def metrics():
    """Scrape endpoint para Prometheus"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/api/v1/workouts", status_code=status.HTTP_201_CREATED)
def record_workout(workout_type: str = "Running"):
    """Registra una nueva sesion de entrenamiento"""
    WORKOUT_COUNTER.labels(workout_type=workout_type).inc()
    return {
        "message": "Sesion de entrenamiento registrada exitosamente",
        "workout_type": workout_type
    }