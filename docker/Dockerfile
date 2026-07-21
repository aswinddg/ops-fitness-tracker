# syntax=docker/dockerfile:1.7

# ==========================================
# STAGE 1: Builder (Compilación y Pip Install)
# ==========================================
FROM python:3.11-slim AS builder

WORKDIR /build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Invalidation Layer Optimization: Dependencias primero
COPY src/requirements.txt .

# 1. Actualiza pip, setuptools y wheel a nivel del sistema base
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# 2. Instala tus dependencias redirigiendo la salida a /install
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --prefix=/install --no-cache-dir -r requirements.txt


# ==========================================
# STAGE 2: Runtime (Hardened & Minimal)
# ==========================================
FROM python:3.11-slim AS final

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.local/bin:${PATH}" \
    PYTHONPATH="/app/src"

# Principio de Menor Privilegio (Non-root user estático)
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/sh -m appuser && \
    apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar paquetes compilados y código fuente asignando owner explícito
COPY --from=builder --chown=appuser:appgroup /install /usr/local
COPY --chown=appuser:appgroup src/ /app/src/

USER 10001:10001

EXPOSE 8000

# Probe interna de salud
HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/healthz || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]