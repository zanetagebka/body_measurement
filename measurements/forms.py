from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.forms import modelformset_factory
from .models import Measurement

class MeasurementForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control', 'required': True},
            format='%Y-%m-%d'
        )
    )
    
    class Meta:
        model = Measurement
        fields = ['date', 'weight', 'waist', 'hips', 'chest', 'thigh', 'calf', 'forearm']
        
        number_input_attrs = {'class': 'form-control', 'step': '0.1'}
        widgets = {
            'weight': forms.NumberInput(attrs=number_input_attrs),
            'waist': forms.NumberInput(attrs=number_input_attrs),
            'hips': forms.NumberInput(attrs=number_input_attrs),
            'chest': forms.NumberInput(attrs=number_input_attrs),
            'thigh': forms.NumberInput(attrs=number_input_attrs),
            'calf': forms.NumberInput(attrs=number_input_attrs),
            'forearm': forms.NumberInput(attrs=number_input_attrs),
        }

# Create a formset for handling multiple measurements
MeasurementFormSet = modelformset_factory(
    Measurement,
    form=MeasurementForm,
    extra=0,
    min_num=1,
    validate_min=True,
    can_delete=False,
    fields=['date', 'weight', 'waist', 'hips', 'chest', 'thigh', 'calf', 'forearm']
)

class LoginForm(AuthenticationForm):
    form_control_attrs = {'class': 'form-control'}
    
    username = forms.CharField(
        label=_("Username"),
        widget=forms.TextInput(attrs={**form_control_attrs, 'placeholder': _('Enter your username')})
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={**form_control_attrs, 'placeholder': _('Enter your password')})
    )

class RegisterForm(UserCreationForm):
    form_control_attrs = {'class': 'form-control'}
    
    username = forms.CharField(
        label=_("Username"),
        widget=forms.TextInput(attrs={**form_control_attrs, 'placeholder': _('Enter your username')})
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={**form_control_attrs, 'placeholder': _('Enter your email')})
    )
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={**form_control_attrs, 'placeholder': _('Enter your password')})
    )
    password2 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(attrs={**form_control_attrs, 'placeholder': _('Confirm your password')})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
