from django.contrib import admin
from .models import WeatherData


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ['location', 'date', 'temperature_avg', 'humidity', 'rainfall', 'wind_speed']
    list_filter = ['location', 'date']
    search_fields = ['location']
    date_hierarchy = 'date'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return ['created_at', 'updated_at']
        return []
