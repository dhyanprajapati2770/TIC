from django.urls import path
from . import views

app_name = 'diseases'

urlpatterns = [
    path('predictor/', views.disease_predictor, name='disease_predictor'),
    path('predict/', views.predict_disease, name='predict_disease'),
    path('result/<int:prediction_id>/', views.disease_result, name='disease_result'),
    path('history/', views.prediction_history, name='prediction_history'),
    path('api/predict/', views.api_predict_disease, name='api_predict_disease'),
]