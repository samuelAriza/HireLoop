# ================================
# Dockerfile - hireloop (PROD)
# ================================

FROM python:3.12-slim

# Evita .pyc y salida buffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copia solo requirements primero (caché)
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia código fuente
COPY . .

# === collectstatic EN BUILD TIME (no en runtime) ===
# Esto evita que el pod espere a la DB para copiar archivos estáticos
RUN python manage.py collectstatic --noinput --clear

# Copia entrypoint y da permisos
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Puerto
EXPOSE 8000

# Entrypoint: espera DB real + inicia Gunicorn
ENTRYPOINT ["/entrypoint.sh"]