from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from main.models import AccountUser, Staff, Child
from django.contrib.auth.models import User
from django.forms import ModelForm

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Phone Number', max_length=30, required=True)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields

class CustomUserCreationForm2(UserCreationForm):
    username = forms.CharField(label="Parent's Phone Number", max_length=30, required=True)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields
        
class AccountUserCreation(ModelForm):
    class Meta:
        model = AccountUser
        fields = ["firstName", "lastName", "gender", "birthDate", "address"]
        widgets = {
            'birthDate': forms.DateInput(attrs={'type': 'date'}),
        }

class StaffUserCreation(ModelForm):
    class Meta:
        model = Staff
        fields = ["NIK", "NPWP", "BankAccount", "BankName"]

class ChildUserCreation(ModelForm):
    dadName = forms.CharField(label='Dad Name', max_length=50, required=True)
    momName = forms.CharField(label='Mom Name', max_length=50, required=True)
    dadJob = forms.CharField(label='Dad Job', max_length=20, required=True)
    momJob = forms.CharField(label='Mom Job', max_length=20, required=True)
    class Meta:
        model = Child
        fields = ["dadName", "momName", "dadJob", "momJob"]
    