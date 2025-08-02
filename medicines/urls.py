from django.urls import path
from . import views

app_name = 'medicines'

urlpatterns = [
    path('search/', views.medicine_search, name='medicine_search'),
    path('recommendations/', views.medicine_recommendations, name='medicine_recommendations'),
    path('detail/<int:medicine_id>/', views.medicine_detail, name='medicine_detail'),
    path('api/search/', views.api_medicine_search, name='api_medicine_search'),
    path('api/recommendations/', views.api_medicine_recommendations, name='api_medicine_recommendations'),
]