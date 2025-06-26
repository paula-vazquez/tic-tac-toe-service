# Usa imagen oficial de Python 3.12 ligera
FROM python:3.12-slim

# Fija directorio de trabajo
WORKDIR /app
ENV PYTHONPATH=/app/src

# Copia requirements y instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la app
COPY . .

# Dar permiso de ejecución al entrypoint
RUN chmod +x /app/entrypoint.sh

# Expone el puerto donde corre Uvicorn
EXPOSE 8000

# Por defecto ejecuta el entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
