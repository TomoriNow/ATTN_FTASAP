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
    if account.is_staff:
        return render(request, 'driver_dashboard.html', {})

def register_driver(request):
    if request.method == "POST":
        form = CustomUserCreationForm2(request.POST)
        form2 = AccountUserCreation(request.POST)
        form3 = StaffUserCreation(request.POST)
        if form.is_valid() and form2.is_valid() and form3.is_valid():
            user = form.save(commit=False)
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
    return render(request, 'register_driver.html', context)

def register_caregiver(request):
    return render(request, 'register_caregiver.html', {})

def daily_report_child(request):
    return render(request, 'daily_report_child.html', {})

def child_list(request):
    return render(request, 'child_list.html', {})

def new_activity_schedule(request):
    return render(request, 'new_activity_schedule.html', {})

def new_menu_schedule(request):
    return render(request, 'new_menu_schedule.html', {})

def new_offered_program(request):
    return render(request, 'new_offered_program.html', {})

def offered_program_detail(request):
    return render(request, 'offered_program_detail.html', {})

def offered_program(request):
    return render(request, 'offered_program.html', {})

def crud_extracurricular(request):
    return render(request, 'crud_extracurricular.html', {})

def activity(request):
    return render(request, 'activity.html', {})

def extracurricular_detail(request):
    return render(request, 'extracurricular_detail.html', {})


def add_extracurricular(request):
    return render(request, 'extracurricular_form.html', {})

def update_extracurricular(request):
    return render(request, 'update_extracurricular.html', {})

def child_payment(request):
    return render(request, 'child_payment.html', {})
    
def payment_history(request):
    return render(request, 'payment_history.html', {})

def create_activity(request):
    return render(request, 'create_activity.html', {})

def update_activity(request):
    return render(request, 'update_activity.html', {})

def program(request):
    return render(request, 'program.html', {})

def pickup_schedule(request):
    return render(request, 'pickup_schedule.html', {})

def manage_extracurricular(request):
    return render(request, 'manage_extracurricular.html', {})

def display_dad_name(request, dadName):
    # You can use dadName in the template or perform any other logic
    context = {'dadName': dadName}
    return render(request, 'display_dad_name.html', context)
        