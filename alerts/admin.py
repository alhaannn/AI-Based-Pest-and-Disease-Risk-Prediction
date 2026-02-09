from django.contrib import admin
from .models import Alert, PreventiveMeasure


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['prediction', 'severity', 'is_read', 'created_at']
    list_filter = ['severity', 'is_read', 'created_at']
    search_fields = ['message', 'prediction__crop__name', 'prediction__pest__name']
    date_hierarchy = 'created_at'
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected alerts as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected alerts as unread"


@admin.register(PreventiveMeasure)
class PreventiveMeasureAdmin(admin.ModelAdmin):
    list_display = ['action', 'pest', 'effectiveness', 'timing']
    list_filter = ['effectiveness', 'pest']
    search_fields = ['action', 'description', 'pest__name']
