from django.urls import path
from . import views

app_name = 'healthcare'

urlpatterns = [
    path('', views.home, name='home'),
    path('health-profile/', views.health_profile, name='health_profile'),
    path('appointments/', views.appointments, name='appointments'),
    path('health-records/', views.health_records, name='health_records'),
    path('vital-signs/', views.vital_signs, name='vital_signs'),
]