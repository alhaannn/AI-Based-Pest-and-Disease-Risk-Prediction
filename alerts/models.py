from django.db import models
from django.utils import timezone
from predictions.models import RiskPrediction
from crops.models import Pest


class Alert(models.Model):
    """Model for storing risk alerts"""
    SEVERITY_LEVELS = [
        ('INFO', 'Information'),
        ('WARNING', 'Warning'),
        ('DANGER', 'Danger'),
        ('CRITICAL', 'Critical'),
    ]
    
    prediction = models.ForeignKey(RiskPrediction, on_delete=models.CASCADE, related_name='alerts')
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.severity} Alert - {self.prediction.crop.name}"


class PreventiveMeasure(models.Model):
    """Model for storing preventive measures for pests/diseases"""
    EFFECTIVENESS_LEVELS = [
        ('LOW', 'Low Effectiveness'),
        ('MEDIUM', 'Medium Effectiveness'),
        ('HIGH', 'High Effectiveness'),
        ('VERY_HIGH', 'Very High Effectiveness'),
    ]
    
    pest = models.ForeignKey(Pest, on_delete=models.CASCADE, related_name='preventive_measures')
    action = models.CharField(max_length=200, help_text="Name of the preventive action")
    description = models.TextField(help_text="Detailed description of the measure")
    effectiveness = models.CharField(max_length=10, choices=EFFECTIVENESS_LEVELS)
    
    # Timing and application
    timing = models.CharField(max_length=200, blank=True, help_text="When to apply this measure")
    dosage = models.CharField(max_length=200, blank=True, help_text="Recommended dosage/amount")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-effectiveness', 'action']
    
    def __str__(self):
        return f"{self.action} for {self.pest.name}"
