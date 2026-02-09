from django.shortcuts import render
from predictions.models import RiskPrediction
from alerts.models import Alert


def risk_assessment_report(request):
    """Generate risk assessment report"""
    predictions = RiskPrediction.objects.all().select_related('crop', 'pest').order_by('-risk_score')[:50]
    high_risk = predictions.filter(risk_level='HIGH')
    medium_risk = predictions.filter(risk_level='MEDIUM')
    low_risk = predictions.filter(risk_level='LOW')
    
    context = {
        'predictions': predictions,
        'high_risk': high_risk,
        'medium_risk': medium_risk,
        'low_risk': low_risk,
        'total_predictions': predictions.count(),
    }
    return render(request, 'reports/risk_assessment.html', context)
