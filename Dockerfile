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

# Copia solo requirements primero (mejor uso de caché)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia código fuente
COPY . .

# Da permisos al entrypoint
RUN chmod +x /entrypoint.sh

# Crea directorio para static files
RUN mkdir -p /app/staticfiles

# === collectstatic EN BUILD TIME ===
# Nota: Esto requiere que settings.py no dependa de variables de entorno
# críticas para collectstatic (como SECRET_KEY debe tener default)
RUN python manage.py collectstatic --noinput --clear || \
    echo "⚠️  collectstatic falló - puede que necesite variables de entorno"

# Puerto
EXPOSE 8000

# Entrypoint: espera DB real + inicia Gunicorn
ENTRYPOINT ["/entrypoint.sh"]