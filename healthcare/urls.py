from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    
    # Symptoms and Diseases
    path('symptoms/', views.SymptomListView.as_view(), name='symptoms'),
    path('diseases/', views.DiseaseListView.as_view(), name='diseases'),
    path('diseases/<int:pk>/', views.DiseaseDetailView.as_view(), name='disease-detail'),
    
    # Symptom Checker
    path('symptom-checker/', views.SymptomCheckerView.as_view(), name='symptom-checker'),
    
    # Medicines
    path('medicines/', views.MedicineListView.as_view(), name='medicines'),
    path('medicines/<int:pk>/', views.MedicineDetailView.as_view(), name='medicine-detail'),
    path('medicine-recommendations/', views.MedicineRecommendationView.as_view(), name='medicine-recommendations'),
    
    # Cart
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/items/<int:item_id>/', views.CartItemView.as_view(), name='cart-item'),
    
    # Orders
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('orders/create/', views.CreateOrderView.as_view(), name='create-order'),
    
    # Chat
    path('chat/history/', views.ChatHistoryView.as_view(), name='chat-history'),
    path('chat/bot/', views.ChatBotView.as_view(), name='chat-bot'),
    
    # Prescriptions
    path('prescriptions/', views.PrescriptionListView.as_view(), name='prescriptions'),
    path('prescriptions/<int:pk>/', views.PrescriptionDetailView.as_view(), name='prescription-detail'),
    
    # User Profile
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    
    # Health Statistics
    path('stats/', views.health_stats, name='health-stats'),
    
    # Admin endpoints
    path('admin/symptoms/', views.AdminSymptomView.as_view(), name='admin-symptoms'),
    path('admin/diseases/', views.AdminDiseaseView.as_view(), name='admin-diseases'),
    path('admin/medicines/', views.AdminMedicineView.as_view(), name='admin-medicines'),
]