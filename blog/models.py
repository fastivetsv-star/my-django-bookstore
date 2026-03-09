from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=255) # Назва товару
    price = models.IntegerField()            # Ціна (тільки цілі числа)
    is_active = models.BooleanField(default=True) # Чи є в наявності (Так/Ні)

    def __str__(self):
        return self.title
    
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE) # Зв'язок з товаром
    text = models.CharField(max_length=255) # Текст відгуку

    def __str__(self):
        return f"відгук на {self.product.title}"