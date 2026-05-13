import asyncio
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext as _ 

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter, OrderingFilter 

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer



async def product_list(request):
    products_queryset = Product.objects.all().order_by('-id')
    products = [product async for product in products_queryset]
        
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



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related('category').order_by('id')
    serializer_class = ProductSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'price'] 
    search_fields = ['name']
    ordering_fields = ['price', 'name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]