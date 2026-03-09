from django.contrib import admin
from .models import Post, Product, Review

admin.site.register(Post)
admin.site.register(Review)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_active')
    search_fields = ('title',)