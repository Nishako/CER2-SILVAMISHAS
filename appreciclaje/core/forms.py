from django import forms
from .models import Solicitud
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label='Nombre')
    last_name = forms.CharField(label='Apellido')
    direccion = forms.CharField(label='Dirección')
    telefono = forms.CharField(label='Teléfono')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'direccion', 'telefono', 'password1', 'password2')

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['tipo_material', 'cantidad', 'fecha_estimada']
        widgets = {
            'fecha_estimada': forms.DateInput(attrs={'type': 'date'})
        }
