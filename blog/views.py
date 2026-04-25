from django.shortcuts import render
from django.db.models import Q, Count
from .models import Post, Product
from .forms import ContactForm
from django.http import HttpResponse, Http404 # 👈 Додали Http404
import asyncio 

async def home(request):
    """
    Відображає головну сторінку сайту.
    
    Збирає останні 5 постів та топ-10 найпопулярніших активних товарів 
    (ціною до 5000) з бази даних асинхронно.
    
    Args:
        request (HttpRequest): Об'єкт HTTP-запиту.
        
    Returns:
        HttpResponse: Відрендерений HTML-шаблон 'blog/home.html' з контекстом.
    """
    # 👈 ОПТИМІЗАЦІЯ З AI_REVIEW: Додали сортування та ліміт (5 постів)
    posts_query = Post.objects.order_by('-id')[:5] 
    all_posts = []
    async for post in posts_query:
        all_posts.append(post)

    # 👈 ОПТИМІЗАЦІЯ З AI_REVIEW: Видалили prefetch_related, додали ліміт (10 товарів)
    smart_products_query = Product.objects.filter(
        Q(is_active=True) | Q(price__lt=5000)
    ).annotate(review_count=Count('review')).order_by('-review_count')[:10]

    smart_products = []
    async for product in smart_products_query:
        smart_products.append(product)
    
    return render(request, 'blog/home.html', {
        'posts': all_posts,
        'products': smart_products
    })

async def contact(request):
    """
    Обробляє сторінку контактів.
    
    При POST-запиті валідує форму та повертає повідомлення про успіх.
    При GET-запиті імітує асинхронну затримку та повертає порожню форму.
    
    Args:
        request (HttpRequest): Об'єкт HTTP-запиту.
        
    Returns:
        HttpResponse: Відрендерений HTML-шаблон або текстова відповідь.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            return HttpResponse(f'Дякуємо за повідомлення, {user_email}!')
    else:
        await asyncio.sleep(0.1) 
        form = ContactForm()
    
    return render(request, 'blog/contact.html', {'form': form})

async def product_detail_async(request, pk):
    """
    Відображає детальну сторінку конкретного товару.
    
    Асинхронно шукає товар за його ID (pk). Якщо товар не знайдено,
    генерує виняток Http404 (замість прямого рендеру сторінки).
    
    Args:
        request (HttpRequest): Об'єкт HTTP-запиту.
        pk (int): Первинний ключ (ID) товару.
        
    Returns:
        HttpResponse: Відрендерений HTML-шаблон 'blog/detail.html'.
    """
    try:
        product = await Product.objects.aget(pk=pk)
    except Product.DoesNotExist:
        # 👈 ОПТИМІЗАЦІЯ З AI_REVIEW: рейзимо Http404
        raise Http404("Товар не знайдено")
        
    return render(request, 'blog/detail.html', {'product': product})

def custom_404(request, exception):
    """Кастомний обробник помилки 404 (Сторінку не знайдено)."""
    return render(request, 'errors/404.html', status=404)