# ============================================================
#  Dockerfile — Finca App (Flask)
# ============================================================

FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias primero (capa cacheada)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Crear carpeta para la base de datos (volumen persistente)
RUN mkdir -p /app/instance

# Puerto expuesto
EXPOSE 81

# Comando de arranque
CMD ["python", "run.py"]
