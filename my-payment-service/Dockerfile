FROM python:3.13-slim

WORKDIR /app

# Забороняємо Python писати .pyc файли та буферизувати вивід
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Встановлюємо залежності
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копіюємо весь код
COPY . .