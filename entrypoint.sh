#!/bin/bash
set -e

echo "=== [$(date)] STARTING ENTRYPOINT ==="

# 1. ESPERA AL PROXY (máx 90s)
echo "Waiting for cloud-sql-proxy on 127.0.0.1:5432..."
timeout 90 bash -c '
  until nc -z 127.0.0.1 5432; do
    echo "  → Proxy not ready... sleeping 2s"
    sleep 2
  done
  echo "  → PROXY READY"
' || {
  echo "ERROR: Proxy failed after 90s"
  exit 1
}

# 2. ESPERA A DJANGO DB (máx 60s)
echo "Waiting for Django DB connection..."
timeout 60 bash -c '
  until python -c "
import os, django, sys
from django.db import connection
os.environ.setdefault(\"DJANGO_SETTINGS_MODULE\", \"hireloop.settings\")
django.setup()
connection.cursor().execute(\"SELECT 1\")
sys.exit(0)
  " 2>/dev/null; do
    echo "  → DB not ready... sleeping 2s"
    sleep 2
  done
' || {
  echo "ERROR: Django DB failed after 60s"
  exit 1
}

echo "=== [$(date)] STARTING GUNICORN ==="
exec gunicorn hireloop.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 2 \
  --timeout 30 \
  --access-logfile - \
  --error-logfile - \
  --log-level info