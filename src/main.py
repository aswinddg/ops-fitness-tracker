import time
from fastapi import FastAPI, Response, status, Depends
from sqlalchemy.orm import Session
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from src.middleware import StructuredLoggingMiddleware
from src.database import engine, get_db, Base
from src.models import Workout as WorkoutModel

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ops Fitness Core API",
    description="API for the Ops Fitness Core",
    version="1.1.0",
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

WORKOUT_COUNTER = Counter(
    "fitness_workouts_total",
    "Total de sesiones de entrenamiento registradas",
    ["workout_type"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "Latencia de las peticiones HTTP en segundos",
    ["endpoint"],
)

@app.middleware("http")
async def measure_request_latency(request, call_next):
    """Mide la duración de cada petición HTTP por endpoint."""
    start_time = time.perf_counter()
    response = await call_next(request)
    elapsed_time = time.perf_counter() - start_time
    REQUEST_LATENCY.labels(endpoint=request.url.path).observe(elapsed_time)
    return response

app.add_middleware(StructuredLoggingMiddleware)

@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {
        "system": "Ops Fitness Tracker",
        "status": "online",
        "environment": "production",
    }

@app.get("/healthz", status_code=status.HTTP_200_OK)
def health_check():
    return {
        "status": "healthy",
        "service": "ops-fitness-core"
    }

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/api/v1/workouts", status_code=status.HTTP_201_CREATED)
def record_workout(workout_type: str = "Running", db: Session = Depends(get_db)):
    """Registra una nueva sesion de entrenamiento"""
    WORKOUT_COUNTER.labels(workout_type=workout_type).inc()
    db_workout = WorkoutModel(workout_type=workout_type)
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout

@app.get("/api/v1/workouts", status_code=status.HTTP_200_OK)
def get_workouts(db: Session = Depends(get_db)):
    """Retorna todas las sesiones de entrenamiento registradas"""
    return db.query(WorkoutModel).all()