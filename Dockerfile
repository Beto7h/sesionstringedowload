# Usamos una imagen ligera de Python 3.11
FROM python:3.11-slim

# Evitamos que Python escriba archivos .pyc y forzamos el output en consola
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establecemos el directorio de trabajo
WORKDIR /app

# Instalamos dependencias del sistema necesarias para compilar librerías como psutil
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiamos el archivo de requerimientos e instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código (main.py, configure.py, database.py, etc.)
COPY . .

# Ejecutamos el archivo principal
CMD ["python", "main.py"]
