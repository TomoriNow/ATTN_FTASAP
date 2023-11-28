from django.urls import path
from main.views import *

app_name = 'main'  # Set the app namespace if necessary

urlpatterns = [
    path('', show_main, name='show_main'),
    path('login/', login_user, name='login_user'),
    path('register/', register, name='register'),
    path('register/admin/', register_admin, name='register_admin'),
    path('register/staff/', register_staff, name='register_staff'),
    path('register/child/', register_child, name='register_child'),
    path('register/driver/', register_driver, name='register_driver'),
    path('register/caregiver/', register_caregiver, name='register_caregiver'),
    path('dailyreport/', daily_report_child, name = "daily_report_child"),
    path('childlist/', child_list, name = "child_list"),
    path('dashboard/child', dashboard, name = 'dashboard'),
    path('new-activity/', new_activity_schedule, name = 'new_activity_schedule'),
    path('new-menu/', new_menu_schedule, name = 'new_menu_schedule'),
    path('new-offered-program/', new_offered_program, name = 'new_offered_program'),
    path('offered-program/', offered_program, name = 'offered_program'),
    path('offered-program/1', offered_program_detail, name = 'offered_program_detail'),
    path('crud_extracurricular/', crud_extracurricular, name = 'crud_extracurricular'),
    path('extracurricular_detail/', extracurricular_detail, name = 'extracurricular_detail'),
    path('add_extracurricular/', add_extracurricular, name = 'add_extracurricular'),
    path('update_extracurricular/', update_extracurricular, name = 'update_extracurricular'),
    path('child_payment/', child_payment, name = 'child_payment'),
    path('payment_history/', payment_history, name = 'payment_history'),
    path('activity/', activity, name = 'activity'),
    path('create_activity/', create_activity, name = 'create_activity'),
    path('program/', program, name = 'program'),
    path('pickup_schedule/', pickup_schedule, name = 'pickup_schedule'),
    path('manage_extracurricular/', manage_extracurricular, name = 'manage_extracurricular'),
    path('update_activity/', update_activity, name = 'update_activity'),
]