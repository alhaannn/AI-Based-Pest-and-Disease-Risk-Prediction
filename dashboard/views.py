from django.shortcuts import render
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
import json
from crops.models import Crop, Pest, InfestationRecord
from weather.models import WeatherData
from predictions.models import RiskPrediction
from alerts.models import Alert


def home(request):
    """Main dashboard view"""
    # Get statistics
    total_crops = Crop.objects.count()
    total_pests = Pest.objects.count()
    total_predictions = RiskPrediction.objects.count()
    
    # High risk predictions (last 7 days)
    last_week = timezone.now().date() - timedelta(days=7)
    high_risk_count = RiskPrediction.objects.filter(
        risk_level='HIGH',
        prediction_date__gte=last_week
    ).count()
    
    # Unread alerts
    unread_alerts = Alert.objects.filter(is_read=False).count()
    
    # Recent high-risk predictions
    recent_predictions = RiskPrediction.objects.filter(
        risk_level__in=['HIGH', 'MEDIUM']
    ).select_related('crop', 'pest').order_by('-prediction_date')[:5]
    
    # Recent alerts
    recent_alerts = Alert.objects.filter(
        is_read=False
    ).select_related('prediction__crop', 'prediction__pest').order_by('-created_at')[:5]
    
    # Weather risk conditions
    recent_weather = WeatherData.objects.filter(
        date__gte=last_week
    ).order_by('-date')[:7]
    
    high_risk_weather_days = sum(1 for w in recent_weather if w.is_high_risk_conditions())
    
    # Pest distribution data for chart
    pest_distribution = Pest.objects.values('pest_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Risk trend data (last 30 days)
    last_month = timezone.now().date() - timedelta(days=30)
    risk_trend = []
    for i in range(30, -1, -5):
        date = timezone.now().date() - timedelta(days=i)
        count = RiskPrediction.objects.filter(
            prediction_date=date,
            risk_level='HIGH'
        ).count()
        risk_trend.append({
            'date': date.strftime('%b %d'),
            'count': count
        })
    
    context = {
        'total_crops': total_crops,
        'total_pests': total_pests,
        'total_predictions': total_predictions,
        'high_risk_count': high_risk_count,
        'unread_alerts': unread_alerts,
        'high_risk_weather_days': high_risk_weather_days,
        'recent_predictions': recent_predictions,
        'recent_alerts': recent_alerts,
        'pest_distribution': json.dumps(list(pest_distribution)),
        'risk_trend': json.dumps(risk_trend),
    }
    
    return render(request, 'dashboard/home.html', context)

