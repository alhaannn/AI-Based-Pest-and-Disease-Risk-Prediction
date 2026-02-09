from django import forms
from .models import Crop, Pest, InfestationRecord


class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['name', 'crop_type', 'growth_stage', 'planting_date', 'field_location', 'area_hectares']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Rice Field A'}),
            'crop_type': forms.Select(attrs={'class': 'form-control'}),
            'growth_stage': forms.Select(attrs={'class': 'form-control'}),
            'planting_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'field_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., North Field Block 1'}),
            'area_hectares': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Area in hectares'}),
        }


class PestForm(forms.ModelForm):
    class Meta:
        model = Pest
        fields = ['name', 'pest_type', 'description', 'severity_level', 'affected_crops']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Brown Planthopper'}),
            'pest_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Detailed description...'}),
            'severity_level': forms.Select(attrs={'class': 'form-control'}),
            'affected_crops': forms.CheckboxSelectMultiple(),
        }


class InfestationRecordForm(forms.ModelForm):
    class Meta:
        model = InfestationRecord
        fields = ['crop', 'pest', 'date', 'severity', 'area_affected', 'notes']
        widgets = {
            'crop': forms.Select(attrs={'class': 'form-control'}),
            'pest': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'severity': forms.Select(attrs={'class': 'form-control'}),
            'area_affected': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Area in hectares'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional notes...'}),
        }
