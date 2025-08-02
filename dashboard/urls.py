from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('analytics/', views.analytics, name='analytics'),
    path('reports/', views.reports, name='reports'),
    path('settings/', views.settings, name='settings'),
    path('api/analytics/', views.api_analytics, name='api_analytics'),
    path('api/reports/', views.api_reports, name='api_reports'),
]