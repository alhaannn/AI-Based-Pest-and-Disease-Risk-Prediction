from django.urls import path
from . import views

app_name = 'predictions'

urlpatterns = [
    path('', views.prediction_list, name='prediction_list'),
    path('generate/', views.generate_predictions, name='generate_predictions'),
    path('<int:pk>/', views.prediction_detail, name='prediction_detail'),
    path('analytics/', views.prediction_analytics, name='prediction_analytics'),
    path('export/csv/', views.export_predictions_csv, name='export_predictions_csv'),
    path('export/all/', views.export_all_data_csv, name='export_all_data'),
]
