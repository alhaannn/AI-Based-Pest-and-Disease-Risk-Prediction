from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('risk-assessment/', views.risk_assessment_report, name='risk_assessment_report'),
]
