from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name', 'phone', 'email', 'address']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'address': forms.Textarea(attrs={'placeholder': 'Address', 'rows': 2}),
        }

