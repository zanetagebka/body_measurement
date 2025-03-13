from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.forms import modelformset_factory
from .models import Measurement

class MeasurementForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'required': True
            },
            format='%Y-%m-%d'
        )
    )
    
    class Meta:
        model = Measurement
        fields = ['date', 'weight', 'waist', 'hips', 'chest', 'thigh', 'calf', 'forearm']
        widgets = {
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'waist': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'hips': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'chest': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'thigh': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'calf': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'forearm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
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
    username = forms.CharField(
        label=_("Username"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter your username')})
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Enter your password')})
    )

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label=_("Username"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter your username')})
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Enter your email')})
    )
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Enter your password')})
    )
    password2 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Confirm your password')})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
