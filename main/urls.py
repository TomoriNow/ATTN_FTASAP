from django.urls import path
from main.views import show_main, login_user, register_admin, register, register_staff, dashboard, register_child, register_driver, daily_report_child, child_list, register_caregiver
from main.views import new_activity_schedule, new_menu_schedule, new_offered_program, offered_program, offered_program_detail, extracurricular_detail, add_extracurricular, update_extracurricular
from main.views import child_payment, crud_extracurricular, payment_history, activity, create_activity

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
    path('dashboard/', dashboard, name = 'dashboard'),
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
]