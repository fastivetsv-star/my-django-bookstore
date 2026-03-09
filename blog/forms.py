from django import forms

class ContactForm(forms.Form):
    email = forms.EmailField(label='Ваш email')
    message = forms.CharField(widget=forms.Textarea, label='Сообщение')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError('Пожалуйста, используйте email с доменом @gmail.com')
        return email