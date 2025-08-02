from django.contrib import admin
from .models import (
    UserProfile, Symptom, Disease, Medicine, DiseasePrediction, 
    DiseasePredictionResult, Cart, CartItem, Order, OrderItem, 
    ChatMessage, Prescription, PrescriptionMedicine
)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'gender', 'date_of_birth', 'created_at']
    list_filter = ['gender', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    list_display = ['name', 'severity_level', 'category', 'created_at']
    list_filter = ['severity_level', 'category', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']

@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'risk_level', 'created_at']
    list_filter = ['risk_level', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['symptoms']
    ordering = ['name']

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'generic_name', 'dosage_form', 'price', 'stock_quantity', 'is_active']
    list_filter = ['dosage_form', 'prescription_required', 'is_active', 'created_at']
    search_fields = ['name', 'generic_name', 'manufacturer']
    list_editable = ['price', 'stock_quantity', 'is_active']
    ordering = ['name']

@admin.register(DiseasePrediction)
class DiseasePredictionAdmin(admin.ModelAdmin):
    list_display = ['user', 'confidence_score', 'created_at']
    list_filter = ['confidence_score', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at']
    filter_horizontal = ['symptoms']

@admin.register(DiseasePredictionResult)
class DiseasePredictionResultAdmin(admin.ModelAdmin):
    list_display = ['prediction', 'disease', 'confidence', 'rank']
    list_filter = ['confidence', 'rank']
    search_fields = ['prediction__user__username', 'disease__name']
    ordering = ['prediction', 'rank']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_amount', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'medicine', 'quantity', 'total_price', 'added_at']
    list_filter = ['added_at']
    search_fields = ['cart__user__username', 'medicine__name']
    readonly_fields = ['total_price', 'added_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['order_number', 'user__username', 'phone']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    list_editable = ['status']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'medicine', 'quantity', 'price']
    list_filter = ['order__status']
    search_fields = ['order__order_number', 'medicine__name']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'message_type', 'user', 'timestamp']
    list_filter = ['message_type', 'timestamp']
    search_fields = ['session_id', 'content', 'user__username']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'doctor_name', 'prescribed_date', 'next_visit', 'created_at']
    list_filter = ['prescribed_date', 'created_at']
    search_fields = ['user__username', 'doctor_name', 'diagnosis']
    readonly_fields = ['created_at']

@admin.register(PrescriptionMedicine)
class PrescriptionMedicineAdmin(admin.ModelAdmin):
    list_display = ['prescription', 'medicine', 'dosage', 'frequency', 'duration']
    list_filter = ['frequency', 'duration']
    search_fields = ['prescription__user__username', 'medicine__name']
    ordering = ['prescription', 'medicine']
