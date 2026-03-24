#!/bin/bash

set -e

echo "⏳ Виконуємо автоматичні міграції бази даних (PostgreSQL)..."
python manage.py makemigrations
python manage.py migrate

echo "✅ Міграції успішно застосовано!"

echo "🚀 Запускаємо Django..."
exec "$@"