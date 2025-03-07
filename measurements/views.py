from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils import translation
from django.conf import settings
from django.urls import reverse
from .forms import MeasurementForm, LoginForm, RegisterForm
from .models import Measurement

@login_required
def measurement_list(request):
    measurements = (Measurement.objects
                   .filter(user=request.user)
                   .order_by('date')
                   .select_related())
    return render(request, 'measurements/list.html', {'measurements': measurements})

@login_required
def measurement_add(request):
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            measurement = form.save(commit=False)
            measurement.user = request.user
            measurement.save()
            return redirect('measurement_list')
    else:
        form = MeasurementForm()
    return render(request, 'measurements/add.html', {'form': form})

@login_required
def measurement_delete(request, pk):
    measurement = get_object_or_404(Measurement, pk=pk, user=request.user)
    if request.method == 'POST':
        measurement.delete()
    return redirect('measurement_list')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('measurement_list')
    
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('measurement_list')
    else:
        form = LoginForm()
    return render(request, 'measurements/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('measurement_list')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('measurement_list')
    else:
        form = RegisterForm()
    return render(request, 'measurements/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def switch_language(request):
    lang = request.GET.get('lang')
    if lang in [code for code, name in settings.LANGUAGES]:
        translation.activate(lang)
        response = redirect(request.META.get('HTTP_REFERER', '/'))
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
        return response
    return redirect('measurement_list')

@login_required
def user_profile(request):
    return render(request, 'measurements/profile.html', {
        'user': request.user
    })

