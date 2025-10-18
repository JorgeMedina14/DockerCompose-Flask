# Usar Python 3.11 slim como imagen base
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema para psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivo de requirements
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente de la aplicación
COPY app.py .

# Exponer el puerto 5000
EXPOSE 5000

# Comando por defecto para ejecutar la aplicación
CMD ["python", "app.py"]