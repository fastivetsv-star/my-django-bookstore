from django.shortcuts import render
from django.db.models import Q, Count
from .models import Post, Product
from .forms import ContactForm
from django.http import HttpResponse
import asyncio 

async def home(request):
    posts_query = Post.objects.all()
    all_posts = []
    async for post in posts_query:
        all_posts.append(post)


    smart_products_query = Product.objects.filter(
        Q(is_active=True) | Q(price__lt=5000)
    ).annotate(review_count=Count('review')).prefetch_related('review_set')

    smart_products = []
    async for product in smart_products_query:
        smart_products.append(product)
    
    return render(request, 'blog/home.html', {
        'posts': all_posts,
        'products': smart_products
    })

async def contact(request):
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
    try:
        product = await Product.objects.aget(pk=pk)
    except Product.DoesNotExist:
        return render(request, 'errors/404.html', status=404)
        
    return render(request, 'blog/detail.html', {'product': product})

def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)