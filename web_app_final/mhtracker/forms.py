from django import forms   
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class SignUpForm(forms.Form):
    """Form class for sign up form"""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data['password'] != cleaned_data['confirm_password']:
            raise ValidationError('Passwords do not match')
        
        if User.objects.filter(username=cleaned_data['username']).exists():
            raise ValidationError('Username already exists')
        
