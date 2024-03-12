from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django import forms
from django.forms.widgets import PasswordInput, TextInput

class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser  # Change User to CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'team_name']  # Include your custom field here

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())
        