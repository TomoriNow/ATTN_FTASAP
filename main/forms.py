from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from main.models import AccountUser, Staff
from django.contrib.auth.models import User
from django.forms import ModelForm

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Phone Number', max_length=30, required=True)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields
        
class AccountUserCreation(ModelForm):
    class Meta:
        model = AccountUser
        fields = ["firstName", "lastName", "gender", "birthDate", "address"]

class StaffUserCreation(ModelForm):
    class Meta:
        model = Staff
        fields = ["NIK", "NPWP", "BankAccount", "BankName"]
    