import asyncio
from django.http import JsonResponse
from django.shortcuts import render
from .models import Product
from django.utils.translation import gettext as _ 

async def product_list(request):
    products_queryset = Product.objects.all()
    
    products = []
    async for product in products_queryset:
        products.append(product)
        
    return render(request, 'products/product_list.html', {
        'products': products,
        'title': _("Наш каталог") 
    })

async def async_check_stock(request):
    await asyncio.sleep(3) 
    
    return JsonResponse({
        "status": _("В наявності"), 
        "message": _("Товар знайдено на складі після 3 секунд пошуку")
    })