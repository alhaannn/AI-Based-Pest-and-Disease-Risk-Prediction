from django.urls import path
from . import views

app_name = 'crops'

urlpatterns = [
    # Crop URLs
    path('crops/', views.crop_list, name='crop_list'),
    path('crops/<int:pk>/', views.crop_detail, name='crop_detail'),
    path('crops/create/', views.crop_create, name='crop_create'),
    path('crops/<int:pk>/update/', views.crop_update, name='crop_update'),
    path('crops/<int:pk>/delete/', views.crop_delete, name='crop_delete'),
    
    # Pest URLs
    path('pests/', views.pest_list, name='pest_list'),
    path('pests/<int:pk>/', views.pest_detail, name='pest_detail'),
    path('pests/create/', views.pest_create, name='pest_create'),
    path('pests/<int:pk>/update/', views.pest_update, name='pest_update'),
    path('pests/<int:pk>/delete/', views.pest_delete, name='pest_delete'),
    
    # Infestation Record URLs
    path('infestations/', views.infestation_list, name='infestation_list'),
    path('infestations/create/', views.infestation_create, name='infestation_create'),
    path('infestations/<int:pk>/update/', views.infestation_update, name='infestation_update'),
    path('infestations/<int:pk>/delete/', views.infestation_delete, name='infestation_delete'),
]
