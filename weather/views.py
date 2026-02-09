from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Avg
import json
from .models import WeatherData
from .forms import WeatherDataForm, WeatherImportForm
from .utils import analyze_conditions, get_weather_trend, get_weather_alerts


def weather_dashboard(request):
    """Enhanced weather dashboard with analytics"""
    # Get filter parameters
    location = request.GET.get('location', '')
    days = int(request.GET.get('days', 7))
    
    # Recent weather data
    weather_data = WeatherData.objects.all().order_by('-date')[:30]
    if location:
        weather_data = weather_data.filter(location__icontains=location)
    
    # Analyze conditions
    analysis = analyze_conditions(location=location, days=days)
    
    # Get weather trend for charts
    trend_data = get_weather_trend(location=location, days=30)
    
    # Get weather alerts
    alerts = get_weather_alerts(days=7)
    
    # Get unique locations for filter
    locations = WeatherData.objects.values_list('location', flat=True).distinct()
    
    context = {
        'weather_data': weather_data[:15],  # Show latest 15 records
        'analysis': analysis,
        'trend_data': json.dumps(trend_data),
        'alerts': alerts,
        'locations': locations,
        'selected_location': location,
        'selected_days': days,
    }
    return render(request, 'weather/dashboard.html', context)


def weather_create(request):
    """Add new weather data"""
    if request.method == 'POST':
        form = WeatherDataForm(request.POST)
        if form.is_valid():
            weather = form.save()
            messages.success(request, f'Weather data for {weather.location} on {weather.date} added successfully!')
            return redirect('weather:weather_dashboard')
    else:
        form = WeatherDataForm()
    
    return render(request, 'weather/weather_form.html', {'form': form, 'action': 'Add'})


def weather_update(request, pk):
    """Update existing weather data"""
    weather = get_object_or_404(WeatherData, pk=pk)
    if request.method == 'POST':
        form = WeatherDataForm(request.POST, instance=weather)
        if form.is_valid():
            form.save()
            messages.success(request, 'Weather data updated successfully!')
            return redirect('weather:weather_dashboard')
    else:
        form = WeatherDataForm(instance=weather)
    
    return render(request, 'weather/weather_form.html', {
        'form': form, 
        'action': 'Update',
        'weather': weather
    })


def weather_delete(request, pk):
    """Delete weather data"""
    weather = get_object_or_404(WeatherData, pk=pk)
    if request.method == 'POST':
        weather.delete()
        messages.success(request, 'Weather data deleted successfully!')
        return redirect('weather:weather_dashboard')
    
    return render(request, 'weather/weather_confirm_delete.html', {'weather': weather})


def weather_import(request):
    """Import weather data from CSV"""
    if request.method == 'POST':
        form = WeatherImportForm(request.POST, request.FILES)
        if form.is_valid():
            from .utils import import_weather_from_csv
            
            csv_file = request.FILES['csv_file']
            result = import_weather_from_csv(csv_file)
            
            if result['success']:
                messages.success(
                    request, 
                    f'Successfully imported {result["imported_count"]} weather records!'
                )
                if result['errors']:
                    for error in result['errors'][:5]:  # Show first 5 errors
                        messages.warning(request, error)
            else:
                for error in result['errors']:
                    messages.error(request, error)
            
            return redirect('weather:weather_dashboard')
    else:
        form = WeatherImportForm()
    
    return render(request, 'weather/weather_import.html', {'form': form})


def weather_analysis(request):
    """Detailed weather analysis page"""
    location = request.GET.get('location', '')
    days = int(request.GET.get('days', 30))
    
    analysis = analyze_conditions(location=location, days=days)
    trend_data = get_weather_trend(location=location, days=days)
    
    # Get locations
    locations = WeatherData.objects.values_list('location', flat=True).distinct()
    
    context = {
        'analysis': analysis,
        'trend_data': json.dumps(trend_data),
        'locations': locations,
        'selected_location': location,
        'selected_days': days,
    }
    return render(request, 'weather/analysis.html', context)
