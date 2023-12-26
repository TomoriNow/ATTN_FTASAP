from django.urls import path
from main.views import show_main, login_user, register_admin, register, register_staff, dashboard, register_child, register_driver, daily_report_child, child_list, register_caregiver
from main.views import new_activity_schedule, new_menu_schedule, new_offered_program, offered_program, offered_program_detail, extracurricular_detail, add_extracurricular, update_extracurricular
from main.views import child_payment, crud_extracurricular, payment_history, activity, create_activity, caregiver_dashboard, driver_dashboard, create_room, manage_menu, menu_form, room_form, class_list
from main.views import children_class, child_dailyreport, daily_reportform, logout_user, delete_offered_program, delete_activity
from main.views import *
app_name = 'main'  # Set the app namespace if necessary

urlpatterns = [
    path('', show_main, name='show_main'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name = 'logout_user'),
    path('register/', register, name='register'),
    path('register/admin/', register_admin, name='register_admin'),
    path('register/staff/', register_staff, name='register_staff'),
    path('register/child/', register_child, name='register_child'),
    path('register/driver/', register_driver, name='register_driver'),
    path('register/caregiver/', register_caregiver, name='register_caregiver'),
    path('dailyreport/', daily_report_child, name = "daily_report_child"),
    path('childlist/', child_list, name = "child_list"),
    path('dashboard/', dashboard, name = 'dashboard'),
    path('new-activity/<str:id>/<str:name>/<int:year>', new_activity_schedule, name = 'new_activity_schedule'),
    path('new-menu/<str:id>/<str:name>/<int:year>', new_menu_schedule, name = 'new_menu_schedule'),
    path('new-offered-program/', new_offered_program, name = 'new_offered_program'),
    path('offered-program/', offered_program, name = 'offered_program'),
    path('delete-offered-program/<str:id>/<int:year>', delete_offered_program, name = 'delete_offered_program'),
    path('offered-program/<str:id>/<str:name>/<int:year>', offered_program_detail, name = 'offered_program_detail'),
    path('crud_extracurricular/', crud_extracurricular, name = 'crud_extracurricular'),
    path('delete_extracurricular_user/<str:Eid>/<str:Uid>/<str:pid>/<int:year>/<str:cl>', delete_extracurricular_user, name = 'delete_extracurricular_user'),
    path('extracurricular_detail/<str:id>/<str:name>/<str:day>/<int:hour>', extracurricular_detail, name = 'extracurricular_detail'),
    path('add_extracurricular/', add_extracurricular, name = 'add_extracurricular'),
    path('update_extracurricular/<str:id>/<str:name>/<str:day>/<int:hour>', update_extracurricular, name = 'update_extracurricular'),
    path('child_payment/', child_payment, name = 'child_payment'),
    path('payment_history/', payment_history, name = 'payment_history'),
    path('activity/', activity, name = 'activity'),
    path('create_activity/', create_activity, name = 'create_activity'),
    path('edit_activity/<str:id>/<str:name>', edit_activity, name = 'edit_activity'),
    path('delete_activity/<str:id>', delete_activity, name = 'delete_activity'),
    path('caregiver_dashboard/', caregiver_dashboard, name = 'caregiver_dashboard'),
    path('driver_dashboard/', driver_dashboard, name = 'driver_dashboard'),
    path('create/', create_room, name='create_room'),
    path('manage_menu/', manage_menu, name = 'manage_menu'),
    path('manage_extracurricular/<str:pid>/<int:year>/<str:cl>', manage_extracurricular, name = 'manage_extracurricular'),
    path('menu_form/', menu_form, name = 'menu_form'),
    path('program/', program, name = 'program'),
    path('pickup_schedule/', pickup_schedule, name = 'pickup_schedule'),
    path('room_form/', room_form, name = 'room_form'),
    path('class_list/', class_list, name = 'class_list'),
    path('children_class/', children_class, name = 'children_class'),
    path('child_dailyreport/', child_dailyreport, name = 'child_dailyreport'),
    path('daily_reportform/', daily_reportform, name = 'daily_reportform'),
    path('delete_extracurricular/<str:id>', delete_extracurricular, name = 'delete_extracurricular'),
]