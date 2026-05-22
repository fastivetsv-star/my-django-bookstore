#!/bin/bash

set -e

echo "⏳ Виконуємо міграції бази даних (PostgreSQL)..."
python manage.py migrate

echo "✅ Міграції успішно застосовано!"

echo "🚀 Запускаємо Django через Gunicorn..."
exec gunicorn mysite.wsgi:application --bind 0.0.0.0:10000