#!/bin/sh
set -e

# Wait for DB
until nc -z ${POSTGRES_HOST:-db} ${POSTGRES_PORT:-5432}; do
  echo "⏳ waiting for db..."
  sleep 1
done

python manage.py migrate --noinput || true
python manage.py runserver 0.0.0.0:8000
