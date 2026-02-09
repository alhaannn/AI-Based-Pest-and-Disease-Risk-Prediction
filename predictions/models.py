from django.db import models
from django.utils import timezone
from crops.models import Crop, Pest


class RiskPrediction(models.Model):
    """Model for storing AI-generated risk predictions"""
    RISK_LEVELS = [
        ('LOW', 'Low Risk (0-33)'),
        ('MEDIUM', 'Medium Risk (34-66)'),
        ('HIGH', 'High Risk (67-100)'),
    ]
    
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='predictions')
    pest = models.ForeignKey(Pest, on_delete=models.CASCADE, related_name='predictions')
    
    # Risk score (0-100)
    risk_score = models.DecimalField(max_digits=5, decimal_places=2)
    risk_level = models.CharField(max_length=10, choices=RISK_LEVELS)
    
    # Prediction details
    prediction_date = models.DateField(default=timezone.now)
    
    # Contributing factors (JSON field to store multiple factors)
    factors = models.JSONField(default=dict, help_text="Key factors contributing to the risk")
    
    # Model confidence (0-100)
    confidence = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-prediction_date', '-risk_score']
    
    def __str__(self):
        return f"{self.pest.name} on {self.crop.name} - {self.risk_level} ({self.risk_score}%)"
    
    def save(self, *args, **kwargs):
        # Automatically set risk_level based on risk_score
        if self.risk_score <= 33:
            self.risk_level = 'LOW'
        elif self.risk_score <= 66:
            self.risk_level = 'MEDIUM'
        else:
            self.risk_level = 'HIGH'
        super().save(*args, **kwargs)
