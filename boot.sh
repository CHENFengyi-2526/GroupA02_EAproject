#!/bin/bash
# gunicorn --bind 0.0.0.0:8080 --workers 2 --threads 4 --timeout 120 wsgi:app

#deploy on GKE
cd /app

echo "🚀 Starting Flask with Gunicorn..."

exec gunicorn --bind 0.0.0.0:8080 \
              --workers 2 \
              --threads 4 \
              --timeout 180 \
              --log-level info \
              wsgi:app