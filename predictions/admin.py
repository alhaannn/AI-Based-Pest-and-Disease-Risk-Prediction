from django.contrib import admin
from .models import RiskPrediction


@admin.register(RiskPrediction)
class RiskPredictionAdmin(admin.ModelAdmin):
    list_display = ['crop', 'pest', 'risk_level', 'risk_score', 'confidence', 'prediction_date']
    list_filter = ['risk_level', 'prediction_date', 'pest', 'crop']
    search_fields = ['crop__name', 'pest__name']
    date_hierarchy = 'prediction_date'
    readonly_fields = ['risk_level', 'created_at', 'updated_at']
