from django.urls import path
from . import views

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
    path('form_erasmo/', views.form_view_erasmo, name='form_erasmo'),
    path('form_mentor/', views.form_view_mentor, name='form_mentor'),
    path('success/', views.success, name='success'),
    path('already_filled/', views.already_filled, name='already_filled'),
    path('export_data/', views.export_data, name='export_data'),
    path('show_results/', views.show_results, name='show_results'),
]

