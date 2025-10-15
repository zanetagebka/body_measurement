from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from datetime import datetime
from .forms import MeasurementForm, LoginForm, RegisterForm
from .models import Measurement
from django.contrib import messages
from .constants import MEASUREMENT_FIELDS

@login_required
def measurement_list(request):
    measurements = (Measurement.objects
                   .filter(user=request.user)
                   .order_by('date'))
    return render(request, 'measurements/list.html', {'measurements': measurements})

@login_required
def measurement_add(request):
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            existing_measurement = Measurement.objects.filter(user=request.user, date=date).first()
            
            if existing_measurement and 'confirm_override' not in request.POST:
                request.session['pending_measurement'] = {
                    'date': date.strftime('%Y-%m-%d'),
                    'weight': str(form.cleaned_data['weight'] or ''),
                    'waist': str(form.cleaned_data['waist'] or ''),
                    'hips': str(form.cleaned_data['hips'] or ''),
                    'chest': str(form.cleaned_data['chest'] or ''),
                    'thigh': str(form.cleaned_data['thigh'] or ''),
                    'calf': str(form.cleaned_data['calf'] or ''),
                    'forearm': str(form.cleaned_data['forearm'] or ''),
                }
                
                return render(request, 'measurements/confirm_override.html', {
                    'existing': {
                        'date': existing_measurement.date,
                        'weight': str(existing_measurement.weight or ''),
                        'waist': str(existing_measurement.waist or ''),
                        'hips': str(existing_measurement.hips or ''),
                        'chest': str(existing_measurement.chest or ''),
                        'thigh': str(existing_measurement.thigh or ''),
                        'calf': str(existing_measurement.calf or ''),
                        'forearm': str(existing_measurement.forearm or ''),
                    },
                    'new': request.session['pending_measurement']
                })
            
            if 'confirm_override' in request.POST:
                date_str = request.session.get('pending_measurement', {}).get('date')
                if date_str:
                    date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    measurement = Measurement.objects.get(user=request.user, date=date)
                    for field in MEASUREMENT_FIELDS:
                        setattr(measurement, field, form.cleaned_data[field])
                    measurement.save()
                    
                    request.session.pop('pending_measurement', None)
                    messages.success(request, _('Measurement updated successfully.'))
                    return redirect('measurement_list')
            else:
                measurement = form.save(commit=False)
                measurement.user = request.user
                measurement.save()
                messages.success(request, _('Measurement added successfully.'))
                return redirect('measurement_list')
    else:
        form = MeasurementForm()
    return render(request, 'measurements/add.html', {'form': form})

@login_required
def measurement_edit(request, pk):
    measurement = get_object_or_404(Measurement, pk=pk, user=request.user)
    if request.method == 'POST':
        form = MeasurementForm(request.POST, instance=measurement)
        if form.is_valid():
            form.save()
            messages.success(request, _('Measurement updated successfully.'))
            return redirect('measurement_list')
    else:
        form = MeasurementForm(instance=measurement)
    return render(request, 'measurements/edit.html', {'form': form})


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

 
