from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Alert, PreventiveMeasure
from .utils import generate_alerts_from_predictions, get_alert_summary
from predictions.models import RiskPrediction


def alert_list(request):
    """List all alerts with filtering"""
    # Get filter parameters
    status = request.GET.get('status', '')
    severity = request.GET.get('severity', '')
    
    # Base query
    alerts = Alert.objects.all().select_related(
        'prediction__crop', 
        'prediction__pest'
    ).order_by('-created_at')
    
    # Apply filters
    if status == 'unread':
        alerts = alerts.filter(is_read=False)
    elif status == 'read':
        alerts = alerts.filter(is_read=True)
    
    if severity:
        alerts = alerts.filter(severity=severity)
    
    # Get summary statistics
    summary = get_alert_summary()
    
    context = {
        'alerts': alerts[:50],  # Limit to 50 for performance
        'status': status,
        'severity': severity,
        'summary': summary,
    }
    return render(request, 'alerts/alert_list.html', context)


def alert_dashboard(request):
    """Comprehensive alert dashboard with analytics"""
    import json
    
    # Get time period
    days = int(request.GET.get('days', 7))
    start_date = timezone.now() - timedelta(days=days)
    
    # Get alerts for period
    alerts = Alert.objects.filter(created_at__gte=start_date)
    
    # Statistics
    stats = {
        'total': alerts.count(),
        'unread': alerts.filter(is_read=False).count(),
        'critical': alerts.filter(severity='CRITICAL').count(),
        'danger': alerts.filter(severity='DANGER').count(),
        'warning': alerts.filter(severity='WARNING').count(),
        'info': alerts.filter(severity='INFO').count(),
    }
    
    # Severity distribution
    severity_dist = alerts.values('severity').annotate(count=Count('id'))
    
    # Daily trend
    daily_trend = []
    for i in range(days, -1, -1):
        date = timezone.now().date() - timedelta(days=i)
        count = alerts.filter(created_at__date=date).count()
        daily_trend.append({
            'date': date.strftime('%b %d'),
            'count': count
        })
    
    # Top affected crops
    top_crops = alerts.values('prediction__crop__name').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Top pests
    top_pests = alerts.values('prediction__pest__name').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Recent critical alerts
    critical_alerts = alerts.filter(
        severity='CRITICAL',
        is_read=False
    ).select_related('prediction__crop', 'prediction__pest')[:10]
    
    context = {
        'stats': stats,
        'severity_dist': json.dumps(list(severity_dist)),
        'daily_trend': json.dumps(daily_trend),
        'top_crops': list(top_crops),
        'top_pests': list(top_pests),
        'critical_alerts': critical_alerts,
        'days': days,
    }
    return render(request, 'alerts/dashboard.html', context)


def mark_as_read(request, pk):
    """Mark a single alert as read"""
    alert = get_object_or_404(Alert, pk=pk)
    alert.is_read = True
    alert.save()
    
    messages.success(request, 'Alert marked as read.')
    return redirect('alerts:alert_list')


def mark_all_as_read(request):
    """Mark all alerts as read"""
    if request.method == 'POST':
        count = Alert.objects.filter(is_read=False).update(is_read=True)
        messages.success(request, f'Marked {count} alerts as read.')
    
    return redirect('alerts:alert_list')


def delete_alert(request, pk):
    """Delete an alert"""
    alert = get_object_or_404(Alert, pk=pk)
    
    if request.method == 'POST':
        alert.delete()
        messages.success(request, 'Alert deleted successfully.')
        return redirect('alerts:alert_list')
    
    return render(request, 'alerts/alert_confirm_delete.html', {'alert': alert})


def unread_alert_count(request):
    """API endpoint for unread alert count"""
    count = Alert.objects.filter(is_read=False).count()
    return JsonResponse({'count': count})


def preventive_measures(request):
    """List all preventive measures with filtering"""
    # Get filter parameters
    pest_id = request.GET.get('pest', '')
    effectiveness = request.GET.get('effectiveness', '')
    
    # Base query
    measures = PreventiveMeasure.objects.all().select_related('pest')
    
    # Apply filters
    if pest_id:
        measures = measures.filter(pest_id=pest_id)
    if effectiveness:
        measures = measures.filter(effectiveness=effectiveness)
    
    # Get pests for filter
    from crops.models import Pest
    pests = Pest.objects.all()
    
    context = {
        'measures': measures,
        'pests': pests,
        'selected_pest': pest_id,
        'selected_effectiveness': effectiveness,
    }
    return render(request, 'alerts/preventive_measures.html', context)


def get_recommendations(request, prediction_id):
    """Get preventive measure recommendations for a specific prediction"""
    prediction = get_object_or_404(RiskPrediction, pk=prediction_id)
    
    # Get preventive measures for this pest
    measures = PreventiveMeasure.objects.filter(
        pest=prediction.pest
    ).order_by('-effectiveness', 'timing')
    
    # Categorize by effectiveness
    high_effectiveness = measures.filter(effectiveness='HIGH')
    medium_effectiveness = measures.filter(effectiveness='MEDIUM')
    low_effectiveness = measures.filter(effectiveness='LOW')
    
    context = {
        'prediction': prediction,
        'high_effectiveness': high_effectiveness,
        'medium_effectiveness': medium_effectiveness,
        'low_effectiveness': low_effectiveness,
    }
    return render(request, 'alerts/recommendations.html', context)


def alert_settings(request):
    """Alert notification settings (placeholder for future email/SMS integration)"""
    if request.method == 'POST':
        # This will be implemented when email/SMS is added
        messages.info(request, 'Email/SMS notifications will be available in a future update.')
        return redirect('alerts:alert_dashboard')
    
    context = {
        'email_enabled': False,
        'sms_enabled': False,
    }
    return render(request, 'alerts/settings.html', context)


def generate_alerts_view(request):
    """Manually trigger alert generation from predictions"""
    if request.method == 'POST':
        count = generate_alerts_from_predictions()
        
        if count > 0:
            messages.success(request, f'Generated {count} new alerts from high-risk predictions!')
        else:
            messages.info(request, 'No new high-risk predictions found.')
        
        return redirect('alerts:alert_dashboard')
    
    # GET - show confirmation page
    # Count potential alerts
    today = timezone.now().date()
    high_risk_predictions = RiskPrediction.objects.filter(
        prediction_date=today,
        risk_level='HIGH'
    ).count()
    
    context = {
        'potential_alerts': high_risk_predictions,
    }
    return render(request, 'alerts/generate_alerts.html', context)
