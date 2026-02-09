from django.db import models
from django.utils import timezone


class WeatherData(models.Model):
    """Model for storing weather and environmental conditions"""
    date = models.DateField(default=timezone.now)
    location = models.CharField(max_length=200)
    
    # Temperature data (in Celsius)
    temperature_avg = models.DecimalField(max_digits=5, decimal_places=2)
    temperature_min = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    temperature_max = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Humidity (percentage)
    humidity = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Rainfall (in mm)
    rainfall = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    # Wind speed (in km/h)
    wind_speed = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    # Additional environmental factors
    soil_moisture = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Soil moisture percentage")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['date', 'location']
    
    def __str__(self):
        return f"{self.location} - {self.date}"
    
    def is_high_risk_conditions(self):
        """Check if weather conditions are favorable for pest outbreaks"""
        # High humidity + moderate temperature + recent rainfall = high risk
        if self.humidity > 70 and 20 <= self.temperature_avg <= 30 and self.rainfall > 5:
            return True
        return False
