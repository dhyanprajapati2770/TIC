from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    UserProfile, Symptom, Disease, Medicine, DiseasePrediction, 
    DiseasePredictionResult, Cart, CartItem, Order, OrderItem, 
    ChatMessage, Prescription, PrescriptionMedicine
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'

class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = '__all__'

class DiseaseSerializer(serializers.ModelSerializer):
    symptoms = SymptomSerializer(many=True, read_only=True)
    
    class Meta:
        model = Disease
        fields = '__all__'

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'

class DiseasePredictionResultSerializer(serializers.ModelSerializer):
    disease = DiseaseSerializer(read_only=True)
    
    class Meta:
        model = DiseasePredictionResult
        fields = ['disease', 'confidence', 'rank']

class DiseasePredictionSerializer(serializers.ModelSerializer):
    symptoms = SymptomSerializer(many=True, read_only=True)
    predicted_diseases = DiseasePredictionResultSerializer(source='diseasepredictionresult_set', many=True, read_only=True)
    
    class Meta:
        model = DiseasePrediction
        fields = ['id', 'symptoms', 'predicted_diseases', 'confidence_score', 'created_at']

class CartItemSerializer(serializers.ModelSerializer):
    medicine = MedicineSerializer(read_only=True)
    total_price = serializers.ReadOnlyField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'medicine', 'quantity', 'total_price', 'added_at']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cartitem_set', many=True, read_only=True)
    total_amount = serializers.ReadOnlyField()
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_amount', 'created_at', 'updated_at']

class OrderItemSerializer(serializers.ModelSerializer):
    medicine = MedicineSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'medicine', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['order_number', 'created_at', 'updated_at']

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'session_id', 'message_type', 'content', 'timestamp']
        read_only_fields = ['timestamp']

class PrescriptionMedicineSerializer(serializers.ModelSerializer):
    medicine = MedicineSerializer(read_only=True)
    
    class Meta:
        model = PrescriptionMedicine
        fields = ['id', 'medicine', 'dosage', 'frequency', 'duration', 'instructions']

class PrescriptionSerializer(serializers.ModelSerializer):
    medicines = PrescriptionMedicineSerializer(source='prescriptionmedicine_set', many=True, read_only=True)
    
    class Meta:
        model = Prescription
        fields = '__all__'
        read_only_fields = ['created_at']

# Registration and Login Serializers
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

# Symptom Checker Serializers
class SymptomCheckerSerializer(serializers.Serializer):
    symptoms = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="List of symptom IDs"
    )
    age = serializers.IntegerField(required=False)
    gender = serializers.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=False)

# Medicine Recommendation Serializers
class MedicineRecommendationSerializer(serializers.Serializer):
    disease_id = serializers.IntegerField()
    symptoms = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )

# Cart Management Serializers
class AddToCartSerializer(serializers.Serializer):
    medicine_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)

class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)

# Order Serializers
class CreateOrderSerializer(serializers.Serializer):
    shipping_address = serializers.CharField()
    phone = serializers.CharField()
    payment_method = serializers.CharField(default='COD')

# Chat Serializers
class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField()
    session_id = serializers.CharField(required=False)