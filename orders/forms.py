from django import forms
from .models import Order
from django.utils.translation import gettext_lazy as _ 

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['email']
        labels = {
            'email': _("Ваш Email для чека"),
        }