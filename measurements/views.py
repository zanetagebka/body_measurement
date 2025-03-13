from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse
from django.forms import formset_factory, modelformset_factory
import csv
from datetime import datetime
from io import TextIOWrapper
from .forms import MeasurementForm, LoginForm, RegisterForm, MeasurementFormSet
from .models import Measurement
from django.contrib import messages

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
                    form_fields = ['weight', 'waist', 'hips', 'chest', 'thigh', 'calf', 'forearm']
                    
                    for field in form_fields:
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

@login_required
def export_measurements_csv(request):
    response = HttpResponse(content_type='text/csv')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    response['Content-Disposition'] = f'attachment; filename="measurements_{timestamp}.csv"'
    
    writer = csv.writer(response)
    # Write the header row with translations
    writer.writerow([
        str(_('Data')),
        str(_('Waga')),
        str(_('Talia')),
        str(_('Biodra')),
        str(_('Klatka piersiowa')),
        str(_('Udo')),
        str(_('Łydka')),
        str(_('Przedramię'))
    ])
    
    # Get user's measurements ordered by date
    measurements = Measurement.objects.filter(user=request.user).order_by('date')
    
    # Write the data rows
    for measurement in measurements:
        writer.writerow([
            measurement.date,
            measurement.weight if measurement.weight is not None else '',
            measurement.waist if measurement.waist is not None else '',
            measurement.hips if measurement.hips is not None else '',
            measurement.chest if measurement.chest is not None else '',
            measurement.thigh if measurement.thigh is not None else '',
            measurement.calf if measurement.calf is not None else '',
            measurement.forearm if measurement.forearm is not None else ''
        ])
    
    return response

@login_required
def import_measurements(request):
    if request.method == 'POST':
        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']
            if not csv_file.name.endswith('.csv'):
                return render(request, 'measurements/import.html', {
                    'error': _('Please upload a CSV file.')
                })
            
            try:
                # Read the CSV file content
                csv_content = csv_file.read().decode('utf-8')
                reader = csv.DictReader(csv_content.splitlines(), delimiter=';')
                csv_data = list(reader)  # Convert to list to avoid consuming iterator
                
                if not csv_data:
                    return render(request, 'measurements/import.html', {
                        'error': _('The CSV file is empty or has invalid format.')
                    })
                
                # Create initial data for the formset
                initial_data = []
                duplicate_dates = {}
                
                for row in csv_data:
                    date_str = row.get('Data', '').strip()
                    if not date_str:  # Skip empty rows
                        continue
                        
                    try:
                        # Parse the date from the CSV
                        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                        
                        # Check for existing measurement on this date
                        existing_measurement = Measurement.objects.filter(
                            user=request.user,
                            date=date_obj
                        ).first()
                        
                        # Create measurement data dictionary
                        measurement_data = {
                            'date': date_str,
                            'weight': row.get('Waga', '').strip(),
                            'waist': row.get('Talia', '').strip(),
                            'hips': row.get('Biodra', '').strip(),
                            'chest': row.get('Klatka piersiowa', '').strip(),
                            'thigh': row.get('Udo', '').strip(),
                            'calf': row.get('Łydka', '').strip(),
                            'forearm': row.get('Przedramię', '').strip()
                        }
                        
                        if existing_measurement:
                            # Store both measurements for comparison
                            duplicate_dates[date_str] = {
                                'existing': {
                                    'date': date_str,
                                    'weight': str(existing_measurement.weight) if existing_measurement.weight else '',
                                    'waist': str(existing_measurement.waist) if existing_measurement.waist else '',
                                    'hips': str(existing_measurement.hips) if existing_measurement.hips else '',
                                    'chest': str(existing_measurement.chest) if existing_measurement.chest else '',
                                    'thigh': str(existing_measurement.thigh) if existing_measurement.thigh else '',
                                    'calf': str(existing_measurement.calf) if existing_measurement.calf else '',
                                    'forearm': str(existing_measurement.forearm) if existing_measurement.forearm else '',
                                },
                                'new': measurement_data
                            }
                        else:
                            measurement_data['date'] = date_obj
                            initial_data.append(measurement_data)
                            
                    except ValueError as e:
                        print(f"Invalid date format in CSV: {date_str} - {str(e)}")
                        continue
                
                if duplicate_dates:
                    # Store initial data in session
                    request.session['pending_import_data'] = initial_data
                    request.session['duplicate_dates'] = duplicate_dates
                    # If there are duplicates, show the comparison page
                    return render(request, 'measurements/resolve_duplicates.html', {
                        'duplicate_dates': duplicate_dates
                    })
                
                if not initial_data:
                    return render(request, 'measurements/import.html', {
                        'error': _('No valid records found in the CSV file.')
                    })
                
                # Create formset with initial data
                FormSet = modelformset_factory(Measurement, form=MeasurementForm, extra=len(initial_data))
                formset = FormSet(queryset=Measurement.objects.none(), initial=initial_data)
                return render(request, 'measurements/import.html', {'formset': formset})
                
            except Exception as e:
                print("Error processing CSV:", str(e))
                return render(request, 'measurements/import.html', {
                    'error': _('Error processing CSV file: ') + str(e)
                })
        elif 'resolve_duplicates' in request.POST:
            try:
                # Handle duplicate resolution
                updated_count = 0
                skipped_count = 0
                
                # Get stored duplicate dates from session
                duplicate_dates = request.session.get('duplicate_dates', {})
                
                # Process measurements with duplicates
                for date_str, measurements in duplicate_dates.items():
                    try:
                        choice = request.POST.get(f'choice_{date_str}')
                        if not choice:
                            continue
                            
                        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                        measurement = Measurement.objects.get(user=request.user, date=date_obj)
                        
                        if choice == 'update':
                            # Update existing measurement with new data
                            new_data = measurements['new']
                            fields = ['weight', 'waist', 'hips', 'chest', 'thigh', 'calf', 'forearm']
                            
                            for field in fields:
                                value = new_data.get(field, '').strip()
                                if value:
                                    try:
                                        setattr(measurement, field, float(value))
                                    except (ValueError, TypeError):
                                        continue
                            
                            measurement.save()
                            updated_count += 1
                        else:
                            skipped_count += 1
                    except (Measurement.DoesNotExist, ValueError) as e:
                        print(f"Error processing measurement for date {date_str}: {str(e)}")
                        continue
                
                # Process any remaining non-duplicate records from the session
                pending_data = request.session.get('pending_import_data', [])
                for data in pending_data:
                    try:
                        measurement = Measurement(user=request.user)
                        date_str = data.get('date')
                        if isinstance(date_str, str):
                            measurement.date = datetime.strptime(date_str, '%Y-%m-%d').date()
                        else:
                            measurement.date = date_str
                            
                        fields = ['weight', 'waist', 'hips', 'chest', 'thigh', 'calf', 'forearm']
                        for field in fields:
                            value = data.get(field, '').strip()
                            if value:
                                try:
                                    setattr(measurement, field, float(value))
                                except (ValueError, TypeError):
                                    continue
                        
                        measurement.save()
                        updated_count += 1
                    except Exception as e:
                        print(f"Error saving measurement: {str(e)}")
                        continue
                
                # Clear session data
                request.session.pop('duplicate_dates', None)
                request.session.pop('pending_import_data', None)
                
                messages.success(request, _(
                    f'Successfully imported {updated_count} measurements. '
                    f'{skipped_count} existing measurements were kept unchanged.'
                ))
                return redirect('measurement_list')
            except Exception as e:
                print("Error during duplicate resolution:", str(e))
                messages.error(request, _('Error processing measurements. Please try again.'))
                return redirect('measurement_list')
        else:
            formset = MeasurementFormSet(request.POST, queryset=Measurement.objects.none())
            if formset.is_valid():
                instances = formset.save(commit=False)
                saved_count = 0
                
                for instance in instances:
                    instance.user = request.user
                    instance.save()
                    saved_count += 1
                
                messages.success(request, _(f'Successfully imported {saved_count} measurements.'))
                return redirect('measurement_list')
            else:
                print("Formset errors:", formset.errors)
                return render(request, 'measurements/import.html', {'formset': formset})
    
    return render(request, 'measurements/import.html')

