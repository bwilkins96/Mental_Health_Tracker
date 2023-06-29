from django import forms   
from django.core.exceptions import ValidationError

class SignUpForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data['password'] != cleaned_data['confirm_password']:
            raise ValidationError('Passwords do not match')