#!/bin/sh
sleep 5

# Aplica migraciones
alembic upgrade head

# Arranca FastAPI
exec uvicorn src.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload