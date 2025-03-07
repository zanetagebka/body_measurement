from django.urls import path
from django.shortcuts import redirect
from . import views

def redirect_to_measurements(request):
    if request.user.is_authenticated:
        return redirect('measurement_list')
    return redirect('login')

urlpatterns = [
    path('', redirect_to_measurements, name='home'),
    path('measurements/', views.measurement_list, name='measurement_list'),
    path('measurements/add/', views.measurement_add, name='measurement_add'),
    path('measurements/delete/<int:pk>/', views.measurement_delete, name='measurement_delete'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('switch-language/', views.switch_language, name='switch_language'),
]
