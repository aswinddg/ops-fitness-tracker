# Definición de SLIs y SLOs - Ops Fitness Tracker

Este documento establece formalmente los Indicadores de Nivel de Servicio (SLI) y los Objetivos de Nivel de Servicio (SLO) para la plataforma.

## 1. Disponibilidad (Availability)
* **SLI:** Porcentaje de peticiones HTTP exitosas (códigos 2xx, 3xx y 4xx de cliente válidos) frente al total de peticiones procesadas por la API (excluyendo health checks).
* **SLO:** La disponibilidad de la API debe mantenerse en un **99.9%** medido en ventanas móviles de 30 días.

## 2. Latencia (Latency)
* **SLI:** Tiempo de respuesta (P95) de los endpoints principales de la API (registro y consulta de workouts).
* **SLO:** El **95%** de las peticiones HTTP deben resolverse en menos de **500 milisegundos**.

## 3. Capacidad y Tráfico (Throughput & Monitoring)
* **SLI:** Monitoreo activo de la tasa de peticiones por segundo (RPS) y detección de anomalías de seguridad o picos de tráfico.
* **SLO:** El sistema debe ser capaz de procesar un tráfico base sin degradar la latencia P95, disparando alertas automáticas a través de Alertmanager si la tasa de errores o latencia supera los umbrales críticos.