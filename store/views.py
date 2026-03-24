from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Book
from django.db.models import Q

# Клас для каталогу (з пагінацією)
class BookListView(ListView):
    model = Book
    template_name = 'store/book_list.html'
    context_object_name = 'books'
    paginate_by = 2  # Наша магія тут!

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = Book.objects.select_related('category')  # Оптимізуємо запити до категорій
        if query:
            return queryset.filter(
                Q(title__icontains=query) | Q(author__icontains=query)
            )
        return queryset.all()

# Клас для детальної сторінки однієї книги
class BookDetailView(DetailView):
    model = Book
    template_name = 'store/book_detail.html'
    context_object_name = 'book'

class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    template_name = 'store/book_form.html'
    fields = "__all__"
    success_url = reverse_lazy('store:book_list')
    login_url = '/accounts/login/'

class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    template_name = 'store/book_form.html'
    fields = "__all__"
    success_url = reverse_lazy('store:book_list')
    login_url = '/accounts/login/'

class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'store/book_confirm_delete.html'
    success_url = reverse_lazy('store:book_list')
    login_url = '/accounts/login/'