# AI Coding Agent Instructions

## Project Overview
Django-based web application in early development stage. This document guides AI agents in contributing to this project effectively.

## Technology Stack
- **Framework**: Django (Python web framework)
- **Language**: Python 3.8+
- **Testing**: Place unit and integration tests in `tests/` directory or as `test_*.py` files

## Project Structure (Evolution Pattern)
```
.
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── <project_name>/          # Main Django project package
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI entry point
│   └── __init__.py
├── <app_name>/              # Django apps (one per responsibility)
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── urls.py              # App-specific URLs
│   ├── admin.py             # Django admin config
│   ├── tests.py             # App tests
│   ├── migrations/          # Database migrations
│   └── templates/           # HTML templates
└── .github/copilot-instructions.md
```

## Essential Workflows

### Django Development Commands
```bash
# Create new app
python manage.py startapp <app_name>

# Run migrations
python manage.py migrate

# Create migration for changes
python manage.py makemigrations

# Run development server
python manage.py runserver

# Run tests
python manage.py test

# Create superuser (admin)
python manage.py createsuperuser

# Django shell for interactive queries
python manage.py shell
```

## Critical Conventions

1. **Models**: Define database models in `models.py` with appropriate `Meta` options (verbose_name, ordering)
2. **Views**: Use class-based views (CBVs) where appropriate; keep business logic in models or services
3. **URLs**: Namespace app URLs; include them in main `urls.py` with `path('app/', include('app.urls', namespace='app'))`
4. **Admin**: Always register models in `admin.py` for easy management
5. **Migrations**: Commit migrations; never delete them. Generate descriptive migration names
6. **Settings**: Use environment variables for secrets (not in version control)
7. **Testing**: Write tests early; use Django's `TestCase` for database isolation

## Code Patterns

### Model Example
```python
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Articles'
    
    def __str__(self):
        return self.title
```

### View Example (Class-Based)
```python
from django.views.generic import ListView
from .models import Article

class ArticleListView(ListView):
    model = Article
    paginate_by = 10
    context_object_name = 'articles'
```

## Do's and Don'ts

✓ **DO**: 
- Use Django ORM exclusively (no raw SQL unless critical performance reason)
- Add `help_text` and `verbose_name` to all model fields
- Use `get_object_or_404()` in views
- Create custom managers for complex queries
  
✗ **DON'T**:
- Import models circularly between apps
- Hardcode configuration values (use settings)
- Leave `DEBUG=True` in production settings
- Ignore migration conflicts in version control

## Session-Specific Context
When implementing features, ensure you:
1. Check current `settings.py` for existing configuration
2. Review existing migrations to understand database state
3. Follow the established app structure (create new apps for distinct responsibilities)
4. Update `requirements.txt` when adding dependencies
