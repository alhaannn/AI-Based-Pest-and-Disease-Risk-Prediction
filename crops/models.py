from django.db import models
from django.utils import timezone


class Crop(models.Model):
    """Model for storing crop information"""
    CROP_TYPES = [
        ('CEREAL', 'Cereal'),
        ('VEGETABLE', 'Vegetable'),
        ('FRUIT', 'Fruit'),
        ('LEGUME', 'Legume'),
        ('OILSEED', 'Oilseed'),
        ('OTHER', 'Other'),
    ]
    
    GROWTH_STAGES = [
        ('SEEDLING', 'Seedling'),
        ('VEGETATIVE', 'Vegetative'),
        ('FLOWERING', 'Flowering'),
        ('FRUITING', 'Fruiting'),
        ('MATURITY', 'Maturity'),
        ('HARVEST', 'Harvest'),
    ]
    
    name = models.CharField(max_length=100)
    crop_type = models.CharField(max_length=20, choices=CROP_TYPES)
    growth_stage = models.CharField(max_length=20, choices=GROWTH_STAGES)
    planting_date = models.DateField()
    field_location = models.CharField(max_length=200)
    area_hectares = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-planting_date']
    
    def __str__(self):
        return f"{self.name} - {self.field_location}"


class Pest(models.Model):
    """Model for storing pest and disease information"""
    PEST_TYPES = [
        ('INSECT', 'Insect'),
        ('FUNGAL', 'Fungal Disease'),
        ('BACTERIAL', 'Bacterial Disease'),
        ('VIRAL', 'Viral Disease'),
        ('WEED', 'Weed'),
        ('OTHER', 'Other'),
    ]
    
    SEVERITY_LEVELS = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    
    name = models.CharField(max_length=100)
    pest_type = models.CharField(max_length=20, choices=PEST_TYPES)
    description = models.TextField()
    severity_level = models.CharField(max_length=20, choices=SEVERITY_LEVELS)
    affected_crops = models.ManyToManyField(Crop, related_name='pests', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.pest_type})"


class InfestationRecord(models.Model):
    """Model for storing historical infestation records"""
    SEVERITY_RATING = [
        (1, 'Very Low'),
        (2, 'Low'),
        (3, 'Moderate'),
        (4, 'High'),
        (5, 'Very High'),
    ]
    
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='infestations')
    pest = models.ForeignKey(Pest, on_delete=models.CASCADE, related_name='records')
    date = models.DateField(default=timezone.now)
    severity = models.IntegerField(choices=SEVERITY_RATING)
    area_affected = models.DecimalField(max_digits=10, decimal_places=2, help_text="Area affected in hectares")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.pest.name} on {self.crop.name} - {self.date}"
