from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.weather_dashboard, name='weather_dashboard'),
    path('add/', views.weather_create, name='weather_create'),
    path('<int:pk>/update/', views.weather_update, name='weather_update'),
    path('<int:pk>/delete/', views.weather_delete, name='weather_delete'),
    path('import/', views.weather_import, name='weather_import'),
    path('analysis/', views.weather_analysis, name='weather_analysis'),
]
