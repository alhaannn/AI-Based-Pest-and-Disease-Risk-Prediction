from django import forms
from .models import WeatherData
from django.utils import timezone


class WeatherDataForm(forms.ModelForm):
    class Meta:
        model = WeatherData
        fields = [
            'date', 'location', 'temperature_avg', 'temperature_min', 
            'temperature_max', 'humidity', 'rainfall', 'wind_speed', 'soil_moisture'
        ]
        widgets = {
            'date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date',
                'value': timezone.now().date()
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'e.g., Farm Location, City, Region'
            }),
            'temperature_avg': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Average temperature in °C',
                'step': '0.1'
            }),
            'temperature_min': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Minimum temperature in °C',
                'step': '0.1'
            }),
            'temperature_max': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Maximum temperature in °C',
                'step': '0.1'
            }),
            'humidity': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Humidity percentage (0-100)',
                'step': '0.1'
            }),
            'rainfall': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Rainfall in mm',
                'step': '0.1'
            }),
            'wind_speed': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Wind speed in km/h',
                'step': '0.1'
            }),
            'soil_moisture': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Soil moisture percentage (optional)',
                'step': '0.1'
            }),
        }


class WeatherImportForm(forms.Form):
    """Form for bulk importing weather data from CSV"""
    csv_file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file with columns: date, location, temperature_avg, humidity, rainfall, wind_speed',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv'})
    )


class WeatherAPIForm(forms.Form):
    """Form for fetching weather data from API"""
    location = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter city name or coordinates'
        })
    )
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
