from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from products.models import Product
from .cart import Cart # Імпортуємо твій клас кошика

@require_POST 
def cart_add(request, product_id):
    cart = Cart(request) 
    product = get_object_or_404(Product, id=product_id) 
    
    cart.add(product=product) 
    

    return redirect('product_list')