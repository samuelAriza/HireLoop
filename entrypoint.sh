#!/bin/bash
set -e

echo "Waiting for Cloud SQL Proxy to be ready on 127.0.0.1:5432..."

# Máximo 60 segundos de espera
for i in {1..30}; do
    if nc -z 127.0.0.1 5432 2>/dev/null; then
        echo "Cloud SQL Proxy is UP!"
        break
    else
        echo "Attempt $i/30: Proxy not ready yet... waiting 2s"
        sleep 2
    fi
done

# Si no conecta, falla el contenedor
if ! nc -z 127.0.0.1 5432 2>/dev/null; then
    echo "ERROR: Could not connect to Cloud SQL Proxy after 60 seconds"
    exit 1
fi

echo "Running collectstatic..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn hireloop.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --access-logfile - \
    --error-logfile - \
    --log-level info