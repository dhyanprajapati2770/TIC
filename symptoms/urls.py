from django.urls import path
from . import views

app_name = 'symptoms'

urlpatterns = [
    path('checker/', views.symptom_checker, name='symptom_checker'),
    path('check/', views.check_symptoms, name='check_symptoms'),
    path('history/', views.symptom_history, name='symptom_history'),
    path('api/symptoms/', views.symptom_list, name='symptom_list'),
    path('api/check/', views.api_check_symptoms, name='api_check_symptoms'),
]