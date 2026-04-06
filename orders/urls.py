from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('success/', views.success_view, name='success'),
    path('cancel/', views.cancel_view, name='cancel'),
    path('webhook/', views.stripe_webhook_view, name='webhook'),
    path('add-test/', views.add_test_product),
]