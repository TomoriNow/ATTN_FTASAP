from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from main.forms import CustomUserCreationForm
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
            response = HttpResponseRedirect(reverse("main:show_main")) 
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
            user.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login_user')
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'register_admin.html', context)