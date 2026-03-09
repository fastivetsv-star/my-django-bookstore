from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Назва категорії')
    slug = models.SlugField(unique=True, verbose_name='URL-адреса категорії')

    def __str__(self):
        return self.name

class Book (models.Model):
    title = models.CharField(max_length=200, verbose_name='Назва книги')
    author = models.CharField(max_length=100, verbose_name='Автор')
    description = models.TextField(verbose_name='Опис')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Ціна')
    stok = models.IntegerField(verbose_name='Кількість на складі')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books', verbose_name='Категорія')

    def __str__(self):
        return self.title