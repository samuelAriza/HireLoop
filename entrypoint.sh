#!/bin/bash
set -e

echo "=== Waiting for REAL database connection ==="

# Intenta conectar con Django (no solo nc)
for i in {1..30}; do
    if python -c "
import sys, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hireloop.settings', default='')
import django
django.setup()
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
    print('DB connected')
    sys.exit(0)
except Exception as e:
    print(f'DB not ready: {e}')
    sys.exit(1)
    " 2>/dev/null; then
        echo "Database is READY!"
        break
    else
        echo "Attempt $i/30: DB not ready... waiting 2s"
        sleep 2
    fi
done

# Si falla después de 30 intentos
if ! python -c "import django, os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hireloop.settings'); django.setup(); from django.db import connection; connection.cursor().execute('SELECT 1')" 2>/dev/null; then
    echo "ERROR: Could not connect to database after 60 seconds"
    exit 1
fi

echo "Starting Gunicorn..."
exec gunicorn hireloop.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --timeout 30