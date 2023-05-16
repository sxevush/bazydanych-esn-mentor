# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('', views.home, name='home'),
#     path('register/', views.register, name='register'),
#     path('login/', views.log_in, name='login'),
#     path('logout/', views.log_out, name='logout'),
#     path('panel/', views.panel, name='panel'),
#     path('edit_profile/', views.edit_profile, name='edit_profile'),
#     path('fill_questionnaire/', views.fill_questionnaire, name='fill_questionnaire'),
#     #path('fill_questionnaire/<int:questionnaire_id>/', views.fill_questionnaire, name='fill_questionnaire'),
#     path('admin_panel/', views.admin_panel, name='admin_panel'),
# ]
from django.urls import path, include
from . import views
#from .views import ten_question_form_list

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('panel/', views.panel, name='panel'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('fill_questionnaire/', views.fill_questionnaire, name='fill_questionnaire'),
    path('edit_questionnaire/', views.edit_questionnaire, name='edit_questionnaire'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    #path('my_view/', views.my_view, name='my_form'),
    path('form_erasmo/', views.form_view_erasmo, name='form_erasmo'),
    path('form_mentor/', views.form_view_mentor, name='form_mentor'),
    path('success/', views.success, name='success'),
    path('already_filled/', views.already_filled, name='already_filled'),
    path('export_data/', views.export_data, name='export_data'),
    path('show_results/', views.show_results, name='show_results'),
]
    #path('ten_question_forms/', ten_question_form_list, name='ten_question_form_list'),

