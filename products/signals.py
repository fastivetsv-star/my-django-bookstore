from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Product

@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    """
    Видаляє застарілі дані про товар з Redis-кешу, якщо товар було змінено.
    """
    cache_key = f'product_detail_{instance.id}'
    
    cache.delete(cache_key)
    
    print(f"🧹 КЕШ ОЧИЩЕНО: Дані для товару '{instance.name}' (ID: {instance.id}) оновлено!")