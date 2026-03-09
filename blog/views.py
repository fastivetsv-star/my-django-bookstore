from django.shortcuts import render
from django.db.models import Q, Count
from .models import Post, Product
from .forms import ContactForm
from django.http import HttpResponse
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

def home(request):
    all_posts = Post.objects.all()
    smart_products = Product.objects.filter(
        Q(is_active=True) | Q(price__lt=5000)
        ).annotate(review_count=Count('review')).prefetch_related('review_set')
    
    return render(request, 'blog/home.html', {
        'posts': all_posts,
        'products': smart_products
    })

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            # Здесь можно обработать данные, например, отправить email
            return HttpResponse(f'Спасибо за ваше сообщение, {user_email}!')
    else:
        form = ContactForm()
    
    return render(request, 'blog/contact.html', {'form': form})

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'blog/detail.html'
    context_object_name = 'product'

    login_url = '/admin/login/'  # URL для перенаправления неавторизованных пользователей

def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)