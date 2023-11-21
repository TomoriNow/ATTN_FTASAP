from django.urls import path
from main.views import main, login_user, register_user

app_name = 'main'  # Set the app namespace if necessary

urlpatterns = [
    path('', main, name='show_main'),
    path('login/', login_user, name='login_user'),
    path('register/', register_user, name='register_user'),
]