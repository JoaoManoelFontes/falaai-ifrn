#!/bin/bash
set -e

echo "📦 Migrando banco..."
python manage.py migrate --noinput

echo "📦 Coletando estáticos..."
python manage.py collectstatic --noinput

echo "🚀 Iniciando aplicação..."
exec "$@"
