"""
Weather analysis utilities for environmental condition assessment
"""
from datetime import timedelta
from django.utils import timezone
from .models import WeatherData


def analyze_conditions(location=None, days=7):
    """
    Analyze weather conditions for the specified location and time period
    Returns risk assessment and key metrics
    """
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)
    
    # Get weather data
    weather_query = WeatherData.objects.filter(date__gte=start_date, date__lte=end_date)
    if location:
        weather_query = weather_query.filter(location__icontains=location)
    
    weather_data = list(weather_query.order_by('-date'))
    
    if not weather_data:
        return {
            'has_data': False,
            'message': 'No weather data available for the specified period'
        }
    
    # Calculate metrics
    avg_temp = sum(w.temperature_avg for w in weather_data) / len(weather_data)
    avg_humidity = sum(w.humidity for w in weather_data) / len(weather_data)
    total_rainfall = sum(w.rainfall for w in weather_data)
    avg_wind_speed = sum(w.wind_speed for w in weather_data) / len(weather_data)
    
    # Risk assessment
    high_risk_days = sum(1 for w in weather_data if w.is_high_risk_conditions())
    risk_percentage = (high_risk_days / len(weather_data)) * 100
    
    # Determine overall risk level
    if risk_percentage >= 50:
        risk_level = 'HIGH'
        risk_color = 'danger'
    elif risk_percentage >= 30:
        risk_level = 'MEDIUM'
        risk_color = 'warning'
    else:
        risk_level = 'LOW'
        risk_color = 'success'
    
    # Identify risk factors
    risk_factors = []
    if avg_humidity > 70:
        risk_factors.append('High average humidity (>70%)')
    if total_rainfall > 50:
        risk_factors.append(f'Significant rainfall ({total_rainfall:.1f}mm in {days} days)')
    if 20 <= avg_temp <= 30:
        risk_factors.append('Optimal temperature range for pest activity')
    
    return {
        'has_data': True,
        'days_analyzed': len(weather_data),
        'avg_temperature': round(avg_temp, 1),
        'avg_humidity': round(avg_humidity, 1),
        'total_rainfall': round(total_rainfall, 1),
        'avg_wind_speed': round(avg_wind_speed, 1),
        'high_risk_days': high_risk_days,
        'risk_percentage': round(risk_percentage, 1),
        'risk_level': risk_level,
        'risk_color': risk_color,
        'risk_factors': risk_factors,
    }


def get_weather_trend(location=None, days=30):
    """
    Get weather trend data for charting
    """
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)
    
    weather_query = WeatherData.objects.filter(date__gte=start_date, date__lte=end_date)
    if location:
        weather_query = weather_query.filter(location__icontains=location)
    
    weather_data = weather_query.order_by('date')
    
    trend_data = {
        'dates': [],
        'temperatures': [],
        'humidity': [],
        'rainfall': [],
        'risk_status': [],
    }
    
    for weather in weather_data:
        trend_data['dates'].append(weather.date.strftime('%b %d'))
        trend_data['temperatures'].append(float(weather.temperature_avg))
        trend_data['humidity'].append(float(weather.humidity))
        trend_data['rainfall'].append(float(weather.rainfall))
        trend_data['risk_status'].append(1 if weather.is_high_risk_conditions() else 0)
    
    return trend_data


def check_pest_favorable_conditions(temperature, humidity, rainfall):
    """
    Check if current conditions are favorable for pest outbreaks
    Returns dict with assessment details
    """
    favorable_factors = []
    warnings = []
    
    # Temperature check
    if 20 <= temperature <= 30:
        favorable_factors.append('Temperature is in optimal range for pest activity (20-30°C)')
    elif temperature > 30:
        warnings.append('High temperature may reduce some pest activity')
    elif temperature < 15:
        warnings.append('Low temperature may slow pest development')
    
    # Humidity check
    if humidity > 70:
        favorable_factors.append('High humidity favors fungal diseases and many pests')
    elif humidity > 60:
        favorable_factors.append('Moderate humidity - some pest risk')
    
    # Rainfall check
    if rainfall > 10:
        favorable_factors.append('Recent significant rainfall increases disease risk')
    
    # Overall assessment
    risk_score = 0
    if 20 <= temperature <= 30:
        risk_score += 30
    if humidity > 70:
        risk_score += 40
    if rainfall > 5:
        risk_score += 30
    
    if risk_score >= 70:
        risk_level = 'HIGH'
    elif risk_score >= 40:
        risk_level = 'MEDIUM'
    else:
        risk_level = 'LOW'
    
    return {
        'risk_score': risk_score,
        'risk_level': risk_level,
        'favorable_factors': favorable_factors,
        'warnings': warnings,
    }


def get_weather_alerts(days=7):
    """
    Generate weather-based alerts for recent high-risk conditions
    """
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)
    
    weather_data = WeatherData.objects.filter(
        date__gte=start_date,
        date__lte=end_date
    ).order_by('-date')
    
    alerts = []
    
    for weather in weather_data:
        if weather.is_high_risk_conditions():
            alert = {
                'date': weather.date,
                'location': weather.location,
                'temperature': weather.temperature_avg,
                'humidity': weather.humidity,
                'rainfall': weather.rainfall,
                'message': f'High-risk conditions detected at {weather.location} on {weather.date}'
            }
            alerts.append(alert)
    
    return alerts


def import_weather_from_csv(csv_file):
    """
    Import weather data from CSV file
    Expected columns: date, location, temperature_avg, humidity, rainfall, wind_speed
    """
    import csv
    from io import TextIOWrapper
    
    imported_count = 0
    errors = []
    
    try:
        # Decode the file
        file_data = TextIOWrapper(csv_file, encoding='utf-8')
        reader = csv.DictReader(file_data)
        
        for row_num, row in enumerate(reader, start=2):
            try:
                weather_data = WeatherData(
                    date=row['date'],
                    location=row['location'],
                    temperature_avg=float(row['temperature_avg']),
                    humidity=float(row['humidity']),
                    rainfall=float(row.get('rainfall', 0)),
                    wind_speed=float(row.get('wind_speed', 0)),
                )
                weather_data.save()
                imported_count += 1
            except Exception as e:
                errors.append(f'Row {row_num}: {str(e)}')
        
        return {
            'success': True,
            'imported_count': imported_count,
            'errors': errors
        }
    
    except Exception as e:
        return {
            'success': False,
            'imported_count': 0,
            'errors': [f'File error: {str(e)}']
        }
