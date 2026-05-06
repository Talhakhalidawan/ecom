from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone")
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'e.g. Alexander'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'e.g. McQueen'}),
            'phone': forms.TextInput(attrs={'placeholder': '+1 (555) 000-0000'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add placeholders for password fields which are inherited from UserCreationForm
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs['placeholder'] = 'Create a secure password'
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your password'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email
