from django.urls import path
from main.views import show_main, login_user, register_admin, register

app_name = 'main'  # Set the app namespace if necessary

urlpatterns = [
    path('', show_main, name='show_main'),
    path('login/', login_user, name='login_user'),
    path('register/', register, name='register'),
    path('register/admin/', register_admin, name='register_admin'),
]