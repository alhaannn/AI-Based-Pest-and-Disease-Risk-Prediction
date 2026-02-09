from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Q
from .models import RiskPrediction
from .ml_engine import generate_predictions_for_all_crops
from crops.models import Crop, Pest


def prediction_list(request):
    """List all risk predictions with filtering"""
    # Get filter parameters
    risk_level = request.GET.get('risk_level', '')
    crop_id = request.GET.get('crop', '')
    pest_id = request.GET.get('pest', '')
    
    # Base query
    predictions = RiskPrediction.objects.all().select_related('crop', 'pest').order_by('-prediction_date', '-risk_score')
    
    # Apply filters
    if risk_level:
        predictions = predictions.filter(risk_level=risk_level)
    if crop_id:
        predictions = predictions.filter(crop_id=crop_id)
    if pest_id:
        predictions = predictions.filter(pest_id=pest_id)
    
    # Get filter options
    crops = Crop.objects.all()
    pests = Pest.objects.all()
    
    # Get statistics
    stats = {
        'total': predictions.count(),
        'high_risk': predictions.filter(risk_level='HIGH').count(),
        'medium_risk': predictions.filter(risk_level='MEDIUM').count(),
        'low_risk': predictions.filter(risk_level='LOW').count(),
    }
    
    context = {
        'predictions': predictions[:50],  # Limit to 50 for performance
        'crops': crops,
        'pests': pests,
        'risk_level': risk_level,
        'selected_crop': crop_id,
        'selected_pest': pest_id,
        'stats': stats,
    }
    return render(request, 'predictions/prediction_list.html', context)


def generate_predictions(request):
    """Generate new predictions using ML engine"""
    if request.method == 'POST':
        try:
            # Generate predictions
            count = generate_predictions_for_all_crops()
            
            if count > 0:
                messages.success(
                    request,
                    f'Successfully generated {count} new risk predictions using AI analysis!'
                )
            else:
                messages.info(
                    request,
                    'Predictions updated. No new high-risk scenarios detected.'
                )
            
            # Auto-generate alerts for high-risk predictions
            from alerts.utils import generate_alerts_from_predictions
            alert_count = generate_alerts_from_predictions()
            
            if alert_count > 0:
                messages.warning(
                    request,
                    f'⚠️ {alert_count} new high-risk alerts generated!'
                )
            
            return redirect('predictions:prediction_list')
        
        except Exception as e:
            messages.error(request, f'Error generating predictions: {str(e)}')
            return redirect('predictions:generate_predictions')
    
    # GET request - show generation page
    from crops.models import Crop, Pest
    from weather.models import WeatherData
    from datetime import timedelta
    from django.utils import timezone
    
    # Get data availability stats
    total_crops = Crop.objects.count()
    total_pests = Pest.objects.count()
    
    last_week = timezone.now().date() - timedelta(days=7)
    recent_weather = WeatherData.objects.filter(date__gte=last_week).count()
    
    from crops.models import InfestationRecord
    historical_records = InfestationRecord.objects.count()
    
    # Check if we have enough data
    has_sufficient_data = total_crops > 0 and total_pests > 0
    
    context = {
        'total_crops': total_crops,
        'total_pests': total_pests,
        'total_combinations': total_crops * total_pests,  # Add multiplication result
        'recent_weather': recent_weather,
        'historical_records': historical_records,
        'has_sufficient_data': has_sufficient_data,
    }
    return render(request, 'predictions/generate_predictions.html', context)


def prediction_detail(request, pk):
    """View detailed prediction information"""
    from django.shortcuts import get_object_or_404
    
    prediction = get_object_or_404(RiskPrediction, pk=pk)
    
    # Get related historical data
    from crops.models import InfestationRecord
    historical_records = InfestationRecord.objects.filter(
        crop=prediction.crop,
        pest=prediction.pest
    ).order_by('-date')[:10]
    
    # Get recent weather data
    from weather.models import WeatherData
    from datetime import timedelta
    from django.utils import timezone
    
    last_week = timezone.now().date() - timedelta(days=7)
    recent_weather = WeatherData.objects.filter(date__gte=last_week).order_by('-date')[:7]
    
    # Get preventive measures
    from alerts.models import PreventiveMeasure
    preventive_measures = PreventiveMeasure.objects.filter(pest=prediction.pest)
    
    context = {
        'prediction': prediction,
        'historical_records': historical_records,
        'recent_weather': recent_weather,
        'preventive_measures': preventive_measures,
    }
    return render(request, 'predictions/prediction_detail.html', context)


def prediction_analytics(request):
    """Analytics dashboard for predictions"""
    import json
    from django.db.models import Avg, Count
    from datetime import timedelta
    from django.utils import timezone
    
    # Get predictions from last 30 days
    last_month = timezone.now().date() - timedelta(days=30)
    predictions = RiskPrediction.objects.filter(prediction_date__gte=last_month)
    
    # Risk distribution
    risk_distribution = predictions.values('risk_level').annotate(count=Count('id'))
    
    # Top risky crops
    top_crops = predictions.filter(risk_level='HIGH').values('crop__name').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Top pests
    top_pests = predictions.filter(risk_level='HIGH').values('pest__name').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Daily trend
    daily_trend = []
    for i in range(30, -1, -1):
        date = timezone.now().date() - timedelta(days=i)
        high_risk = predictions.filter(prediction_date=date, risk_level='HIGH').count()
        daily_trend.append({
            'date': date.strftime('%b %d'),
            'count': high_risk
        })
    
    # Average confidence by risk level
    avg_confidence = predictions.values('risk_level').annotate(
        avg_conf=Avg('confidence')
    )
    
    context = {
        'risk_distribution': json.dumps(list(risk_distribution)),
        'top_crops': list(top_crops),
        'top_pests': list(top_pests),
        'daily_trend': json.dumps(daily_trend),
        'avg_confidence': list(avg_confidence),
        'total_predictions': predictions.count(),
    }
    return render(request, 'predictions/analytics.html', context)


def export_predictions_csv(request):
    """Export predictions to CSV"""
    import csv
    from django.http import HttpResponse
    from datetime import datetime
    
    # Get filter parameters (same as list view)
    risk_level = request.GET.get('risk_level', '')
    crop_id = request.GET.get('crop', '')
    pest_id = request.GET.get('pest', '')
    
    # Base query
    predictions = RiskPrediction.objects.all().select_related('crop', 'pest').order_by('-prediction_date', '-risk_score')
    
    # Apply filters
    if risk_level:
        predictions = predictions.filter(risk_level=risk_level)
    if crop_id:
        predictions = predictions.filter(crop_id=crop_id)
    if pest_id:
        predictions = predictions.filter(pest_id=pest_id)
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="predictions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Prediction Date',
        'Crop Name',
        'Crop Type',
        'Growth Stage',
        'Pest/Disease Name',
        'Pest Type',
        'Risk Score (%)',
        'Risk Level',
        'Confidence (%)',
        'Contributing Factors'
    ])
    
    for pred in predictions:
        writer.writerow([
            pred.prediction_date.strftime('%Y-%m-%d'),
            pred.crop.name,
            pred.crop.get_crop_type_display(),
            pred.crop.get_growth_stage_display(),
            pred.pest.name,
            pred.pest.get_pest_type_display(),
            pred.risk_score,
            pred.get_risk_level_display(),
            pred.confidence,
            pred.contributing_factors or '-'
        ])
    
    return response


def export_all_data_csv(request):
    """Export comprehensive data including crops, pests, weather, and predictions"""
    import csv
    from django.http import HttpResponse
    from datetime import datetime
    import zipfile
    import io
    
    # Create in-memory ZIP file
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # 1. Export Predictions
        pred_buffer = io.StringIO()
        pred_writer = csv.writer(pred_buffer)
        pred_writer.writerow(['Date', 'Crop', 'Pest', 'Risk Score', 'Risk Level', 'Confidence'])
        
        predictions = RiskPrediction.objects.all().select_related('crop', 'pest')
        for pred in predictions:
            pred_writer.writerow([
                pred.prediction_date,
                pred.crop.name,
                pred.pest.name,
                pred.risk_score,
                pred.risk_level,
                pred.confidence
            ])
        zip_file.writestr('predictions.csv', pred_buffer.getvalue())
        
        # 2. Export Crops
        crop_buffer = io.StringIO()
        crop_writer = csv.writer(crop_buffer)
        crop_writer.writerow(['Name', 'Type', 'Growth Stage', 'Planting Date', 'Area (hectares)', 'Location'])
        
        crops = Crop.objects.all()
        for crop in crops:
            crop_writer.writerow([
                crop.name,
                crop.get_crop_type_display(),
                crop.get_growth_stage_display(),
                crop.planting_date,
                crop.area_hectares,
                crop.field_location
            ])
        zip_file.writestr('crops.csv', crop_buffer.getvalue())
        
        # 3. Export Pests
        pest_buffer = io.StringIO()
        pest_writer = csv.writer(pest_buffer)
        pest_writer.writerow(['Name', 'Type', 'Description', 'Severity', 'Affected Crops'])
        
        pests = Pest.objects.all()
        for pest in pests:
            affected_crops_list = ', '.join([c.name for c in pest.affected_crops.all()])
            pest_writer.writerow([
                pest.name,
                pest.get_pest_type_display(),
                pest.description[:200] if pest.description else '',
                pest.get_severity_level_display(),
                affected_crops_list
            ])
        zip_file.writestr('pests.csv', pest_buffer.getvalue())
        
        # 4. Export Weather Data
        from weather.models import WeatherData
        weather_buffer = io.StringIO()
        weather_writer = csv.writer(weather_buffer)
        weather_writer.writerow(['Date', 'Location', 'Temp Min', 'Temp Max', 'Temp Avg', 'Humidity', 'Rainfall', 'Wind Speed'])
        
        weather_data = WeatherData.objects.all().order_by('-date')[:100]  # Last 100 records
        for weather in weather_data:
            weather_writer.writerow([
                weather.date,
                weather.location,
                weather.temperature_min,
                weather.temperature_max,
                weather.temperature_avg,
                weather.humidity,
                weather.rainfall,
                weather.wind_speed
            ])
        zip_file.writestr('weather_data.csv', weather_buffer.getvalue())
        
        # 5. Export Alerts
        from alerts.models import Alert
        alert_buffer = io.StringIO()
        alert_writer = csv.writer(alert_buffer)
        alert_writer.writerow(['Created', 'Severity', 'Message', 'Is Read', 'Crop', 'Pest', 'Risk Score'])
        
        alerts = Alert.objects.all().select_related('prediction__crop', 'prediction__pest').order_by('-created_at')[:100]
        for alert in alerts:
            alert_writer.writerow([
                alert.created_at,
                alert.severity,
                alert.message,
                'Yes' if alert.is_read else 'No',
                alert.prediction.crop.name if alert.prediction else '-',
                alert.prediction.pest.name if alert.prediction else '-',
                alert.prediction.risk_score if alert.prediction else '-'
            ])
        zip_file.writestr('alerts.csv', alert_buffer.getvalue())
    
    # Prepare response
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="pest_prediction_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip"'
    
    return response

