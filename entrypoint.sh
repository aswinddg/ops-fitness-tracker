#!/bin/sh

# Esperar a que la base de datos esté lista (opcional pero recomendado)
echo "Aplicando migraciones de base de datos..."
alembic upgrade head

echo "Iniciando la aplicación..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000