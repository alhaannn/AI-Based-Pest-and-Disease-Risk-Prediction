from django.contrib import admin
from .models import Crop, Pest, InfestationRecord


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ['name', 'crop_type', 'growth_stage', 'planting_date', 'field_location', 'area_hectares']
    list_filter = ['crop_type', 'growth_stage', 'planting_date']
    search_fields = ['name', 'field_location']
    date_hierarchy = 'planting_date'


@admin.register(Pest)
class PestAdmin(admin.ModelAdmin):
    list_display = ['name', 'pest_type', 'severity_level', 'created_at']
    list_filter = ['pest_type', 'severity_level']
    search_fields = ['name', 'description']
    filter_horizontal = ['affected_crops']


@admin.register(InfestationRecord)
class InfestationRecordAdmin(admin.ModelAdmin):
    list_display = ['pest', 'crop', 'date', 'severity', 'area_affected']
    list_filter = ['severity', 'date', 'pest', 'crop']
    search_fields = ['pest__name', 'crop__name', 'notes']
    date_hierarchy = 'date'
