from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from main.models import AccountUser
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Phone Number', max_length=30, required=True)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields