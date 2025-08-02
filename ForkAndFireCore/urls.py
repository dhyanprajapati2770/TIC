"""
URL configuration for ForkAndFireCore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from recipes.views import home, indexpage, recipe2page, featurespage, aboutpage, recipeviewpage, contactpage

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Healthcare API endpoints
    path('api/auth/', include('healthcare_auth.urls')),
    path('api/symptoms/', include('symptom_checker.urls')),
    path('api/disease/', include('disease_predictor.urls')),
    path('api/medicine/', include('medicine_recommendation.urls')),
    path('api/pharmacy/', include('pharmacy.urls')),
    path('api/chat/', include('doctor_chat.urls')),
    path('api/dashboard/', include('user_dashboard.urls')),
    
    # Original recipe app URLs (keeping for backward compatibility)
    path('recipes/home/', home),
    path('recipes/', indexpage),
    path('recipes/recipe2page/', recipe2page),
    path('recipes/indexpage/', indexpage),
    path('recipes/featurespage/', featurespage),
    path('recipes/aboutpage/', aboutpage),
    path('recipes/recipeviewpage/<id>', recipeviewpage),
    path('recipes/contactpage/', contactpage),
    
    # Default route redirects to React app
    path('', indexpage),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_title = "HealthCare+ Admin"
admin.site.site_header = "HealthCare+ Administration"
admin.site.index_title = "Comprehensive Healthcare Management Platform"