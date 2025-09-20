from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border border-gray-300 rounded-lg px-3 py-2 w-full', 'placeholder': 'Votre nom'}),
            'email': forms.EmailInput(attrs={'class': 'border border-gray-300 rounded-lg px-3 py-2 w-full', 'placeholder': 'Votre email'}),
            'subject': forms.TextInput(attrs={'class': 'border border-gray-300 rounded-lg px-3 py-2 w-full', 'placeholder': 'Sujet'}),
            'message': forms.Textarea(attrs={'class': 'border border-gray-300 rounded-lg px-3 py-2 w-full', 'placeholder': 'Votre message', 'rows': 5}),
        }
