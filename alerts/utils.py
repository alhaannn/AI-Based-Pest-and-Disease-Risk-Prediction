"""
Alert generation and management utilities
"""
from django.utils import timezone
from .models import Alert, PreventiveMeasure
from predictions.models import RiskPrediction


def generate_alerts_from_predictions():
    """
    Automatically generate alerts for high-risk predictions
    Returns: number of alerts created
    """
    # Get today's high-risk predictions that don't have alerts yet
    today = timezone.now().date()
    high_risk_predictions = RiskPrediction.objects.filter(
        prediction_date=today,
        risk_level='HIGH'
    )
    
    alerts_created = 0
    
    for prediction in high_risk_predictions:
        # Check if alert already exists
        existing_alert = Alert.objects.filter(
            prediction=prediction,
            created_at__date=today
        ).first()
        
        if not existing_alert:
            # Determine severity based on risk score
            if prediction.risk_score >= 80:
                severity = 'CRITICAL'
            elif prediction.risk_score >= 70:
                severity = 'DANGER'
            else:
                severity = 'WARNING'
            
            # Create alert message
            message = (
                f"High risk of {prediction.pest.name} outbreak detected on {prediction.crop.name}. "
                f"Risk score: {prediction.risk_score}%. "
                f"Immediate preventive action recommended."
            )
            
            # Create alert
            Alert.objects.create(
                prediction=prediction,
                severity=severity,
                message=message,
                is_read=False
            )
            alerts_created += 1
    
    return alerts_created


def get_recommended_actions(pest):
    """
    Get recommended preventive measures for a specific pest
    """
    measures = PreventiveMeasure.objects.filter(pest=pest).order_by('-effectiveness')
    return measures


def mark_alert_as_read(alert_id):
    """
    Mark an alert as read
    """
    try:
        alert = Alert.objects.get(id=alert_id)
        alert.is_read = True
        alert.save()
        return True
    except Alert.DoesNotExist:
        return False


def get_unread_alert_count():
    """
    Get count of unread alerts
    """
    return Alert.objects.filter(is_read=False).count()


def get_critical_alerts():
    """
    Get all critical unread alerts
    """
    return Alert.objects.filter(
        severity='CRITICAL',
        is_read=False
    ).select_related('prediction__crop', 'prediction__pest').order_by('-created_at')


def cleanup_old_alerts(days=30):
    """
    Delete read alerts older than specified days
    """
    from datetime import timedelta
    
    cutoff_date = timezone.now() - timedelta(days=days)
    deleted_count = Alert.objects.filter(
        is_read=True,
        created_at__lt=cutoff_date
    ).delete()[0]
    
    return deleted_count


def create_custom_alert(prediction, severity, message):
    """
    Create a custom alert for a prediction
    """
    alert = Alert.objects.create(
        prediction=prediction,
        severity=severity,
        message=message,
        is_read=False
    )
    return alert


def get_alert_summary():
    """
    Get summary statistics for alerts
    """
    from django.db.models import Count
    
    summary = {
        'total': Alert.objects.count(),
        'unread': Alert.objects.filter(is_read=False).count(),
        'critical': Alert.objects.filter(severity='CRITICAL', is_read=False).count(),
        'by_severity': Alert.objects.values('severity').annotate(count=Count('id')),
    }
    
    return summary
