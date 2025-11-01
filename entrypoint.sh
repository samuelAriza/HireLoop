#!/bin/bash
set -e

echo "=== Waiting for Cloud SQL Proxy to be ready ==="

# Espera a que el proxy abra el puerto
for i in {1..60}; do
    if nc -z 127.0.0.1 5432 2>/dev/null; then
        echo "Cloud SQL Proxy is READY on 127.0.0.1:5432"
        break
    else
        echo "Attempt $i/60: Proxy not ready... waiting 1s"
        sleep 1
    fi
done

if ! nc -z 127.0.0.1 5432 2>/dev/null; then
    echo "ERROR: Cloud SQL Proxy failed to start"
    exit 1
fi

echo "=== Waiting for REAL database connection (Django) ==="

for i in {1..30}; do
    if python -c "
import sys, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hireloop.settings')
import django
django.setup()
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
    sys.exit(0)
except Exception as e:
    print(f'Error: {e}')
    sys.exit(1)
    " >/dev/null 2>&1; then
        echo "Database is READY!"
        break
    else
        echo "Attempt $i/30: DB not ready... waiting 2s"
        sleep 2
    fi
done

echo "Starting Gunicorn..."
exec gunicorn hireloop.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --access-logfile - \
    --error-logfile - \
    --log-level info