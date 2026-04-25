# AI Code Review Report

## View 1: `home` (з `blog/views.py`)

### 1. Оригінальний код
```python
def home(request):
    all_posts = Post.objects.all()
    smart_products = Product.objects.filter(
        Q(is_active=True) | Q(price__lt=5000)
        ).annotate(review_count=Count('review')).prefetch_related('review_set')
    
    return render(request, 'blog/home.html', {
        'posts': all_posts,
        'products': smart_products
    })