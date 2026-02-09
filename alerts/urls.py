from django.urls import path
from . import views

app_name = 'alerts'

urlpatterns = [
    path('', views.alert_list, name='alert_list'),
    path('dashboard/', views.alert_dashboard, name='alert_dashboard'),
    path('<int:pk>/read/', views.mark_as_read, name='mark_as_read'),
    path('mark-all-read/', views.mark_all_as_read, name='mark_all_as_read'),
    path('<int:pk>/delete/', views.delete_alert, name='delete_alert'),
    path('api/unread-count/', views.unread_alert_count, name='unread_alert_count'),
    path('preventive-measures/', views.preventive_measures, name='preventive_measures'),
    path('recommendations/<int:prediction_id>/', views.get_recommendations, name='get_recommendations'),
    path('settings/', views.alert_settings, name='alert_settings'),
    path('generate/', views.generate_alerts_view, name='generate_alerts'),
]
