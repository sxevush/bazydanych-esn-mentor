from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('panel/', views.panel, name='panel'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('form/', views.form_view, name='form'),
    path('success/', views.success, name='success'),
    path('already_filled/', views.already_filled, name='already_filled'),
    path('export_data/', views.export_data, name='export_data'),
    path('mentor_select/', views.mentor_selection_view, name='mentor_select'),
]
