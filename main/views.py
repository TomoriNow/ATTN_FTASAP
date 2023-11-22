from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from main.forms import CustomUserCreationForm, AccountUserCreation, StaffUserCreation, ChildUserCreation, CustomUserCreationForm2
from main.models import AccountUser
from django.contrib import messages
import datetime

def show_main(request):
    return render(request, 'main.html', {})

def register(request):
    return render(request, 'register.html', {})

def login_user(request):
    if request.method == 'POST':
        phoneNo = request.POST.get('phoneNo')
        password = request.POST.get('password')
        user = authenticate(request, username=phoneNo, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:dashboard")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login_user'))
    response.delete_cookie('last_login')
    return redirect('main:login')

def register_admin(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = True  # Set the user as a superuser
            user.is_staff = True
            user.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login_user')
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'register_admin.html', context)

def register_staff(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        form2 = AccountUserCreation(request.POST)
        form3 = StaffUserCreation(request.POST)
        
        if form.is_valid() and form2.is_valid() and form3.is_valid():
            user = form.save(commit=False)
            user.is_staff=True
            user.save()
            account = form2.save(commit=False)
            account.user=user
            account.is_staff=True
            account.save()
            staff = form3.save(commit=False)
            staff.user = account
            staff.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login_user')
    else:
        form = CustomUserCreationForm()
        form2 = AccountUserCreation()
        form3 = StaffUserCreation()

    context = {'form': form, 'form2':form2, 'form3':form3}
    return render(request, 'register_staff.html', context)

def register_child(request):
    if request.method == "POST":
        form = CustomUserCreationForm2(request.POST)
        form2 = AccountUserCreation(request.POST)
        form3 = ChildUserCreation(request.POST)
        
        if form.is_valid() and form2.is_valid() and form3.is_valid():
            user = form.save(commit=False)
            user.save()
            account = form2.save(commit=False)
            account.user=user
            account.is_child=True
            account.save()
            staff = form3.save(commit=False)
            staff.user = account
            staff.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login_user')
    else:
        form = CustomUserCreationForm2()
        form2 = AccountUserCreation()
        form3 = ChildUserCreation()

    context = {'form': form, 'form2':form2, 'form3':form3}
    return render(request, 'register_child.html', context)

def dashboard(request):
    user = request.user
    if user.is_superuser:
        return render(request, 'admin_dashboard.html', {})
    account = AccountUser.objects.get(user = request.user)
    if account.is_child:
        return render(request, 'child_dashboard.html', {})

def register_driver(request):
    return render(request, 'register_driver.html', {})
    
            
        
        