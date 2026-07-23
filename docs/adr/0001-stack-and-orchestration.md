# 1. Elección de Stack, Seguridad y Orquestación de Microservicios

* **Estado:** Aceptado
* **Fecha:** 2026-07-23
* **Contexto:** 
  Se requiere transformar el despliegue manual de `ops-fitness-tracker` en una plataforma automatizada, segura (DevSecOps) y observable a costo inicial $0.

* **Decisión:**
  1. **Framework:** FastAPI por su rendimiento asíncrono nativo y facilidad para instrumentación de métricas.
  2. **Contenedorización:** Dockerfile Multi-stage build con usuario no raíz (ID `10001`) para reducir la superficie de ataque y asegurar cumplimiento en escaneos SAST/SCA con Trivy.
  3. **Orquestación:** Kubernetes (K8s) utilizando manifiestos declarativos (`Deployment`, `Service`, `ConfigMap`, `Ingress`) gestionando límites de recursos (`resources.limits/requests`) y probes de salud.
  4. **Observabilidad:** Exposición de métricas Prometheus en la API y recolección automática mediante servidor Prometheus y visualización en Grafana.

* **Consecuencias:**
  * **Positivas:** Despliegue estandarizado, detección temprana de vulnerabilidades (Shift-Left Security), monitoreo en tiempo real de disponibilidad y cero costo en licencias iniciales.
  * **Mitigaciones:** Requiere conocimiento previo de Kubernetes y sintaxis PromQL para administración de paneles.