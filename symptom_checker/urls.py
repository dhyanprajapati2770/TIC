from django.urls import path
from . import views

urlpatterns = [
    # Symptom management
    path('', views.SymptomListView.as_view(), name='symptom_list'),
    path('categories/', views.get_symptom_categories, name='symptom_categories'),
    
    # Symptom checking
    path('check/', views.submit_symptom_check, name='submit_symptom_check'),
    path('history/', views.get_symptom_history, name='symptom_history'),
    path('check/<int:check_id>/', views.get_symptom_check_detail, name='symptom_check_detail'),
]