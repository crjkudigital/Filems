from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")  # Override to show 'Email' instead of 'Username'
