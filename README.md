# 🚀 Microservice E-commerce Platform (Книжковий магазин)

[![Django CI/CD Pipeline](https://github.com/fastivetsv-star/my-django-bookstore/actions/workflows/django.yml/badge.svg)](https://github.com/fastivetsv-star/my-django-bookstore/actions/workflows/django.yml)
![Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen.svg)

Сучасний інтернет-магазин, розроблений на базі Django. Проєкт еволюціонував у повноцінну **мікросервісну архітектуру** (Project A — Магазин, Project B — Платіжний шлюз) з використанням REST API комунікації, асинхронних views, багатомовності (i18n) та фонових задач. Усе запаковано в єдине середовище Docker Compose.

## 🏗 Архітектурна діаграма

```mermaid
graph TD
    Client[Клієнт / Браузер] --> NGINX[NGINX Reverse Proxy :80]
    NGINX --> ProjectA[Project A: Store backend :8001]
    
    ProjectA --> Redis[(Redis Cache/Broker :6379)]
    ProjectA --> Celery[Celery Workers & Beat]
    ProjectA --> DB_A[(PostgreSQL: store_db)]
    
    ProjectA -- "REST API (HTTP POST)" --> ProjectB[Project B: Payment Gateway :8000]
    ProjectB --> DB_B[(PostgreSQL: payment_db)]