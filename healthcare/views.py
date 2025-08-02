from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
import random
import uuid

from .models import (
    UserProfile, Symptom, Disease, Medicine, DiseasePrediction, 
    DiseasePredictionResult, Cart, CartItem, Order, OrderItem, 
    ChatMessage, Prescription, PrescriptionMedicine
)
from .serializers import (
    UserSerializer, UserProfileSerializer, SymptomSerializer, DiseaseSerializer,
    MedicineSerializer, DiseasePredictionSerializer, CartSerializer, CartItemSerializer,
    OrderSerializer, ChatMessageSerializer, PrescriptionSerializer,
    UserRegistrationSerializer, LoginSerializer, SymptomCheckerSerializer,
    MedicineRecommendationSerializer, AddToCartSerializer, UpdateCartItemSerializer,
    CreateOrderSerializer, ChatRequestSerializer
)

# Authentication Views
class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            UserProfile.objects.create(user=user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'user': UserSerializer(user).data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Symptom and Disease Views
class SymptomListView(generics.ListAPIView):
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer
    permission_classes = [AllowAny]

class DiseaseListView(generics.ListAPIView):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    permission_classes = [AllowAny]

class DiseaseDetailView(generics.RetrieveAPIView):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    permission_classes = [AllowAny]

# Symptom Checker and Disease Prediction
class SymptomCheckerView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = SymptomCheckerSerializer(data=request.data)
        if serializer.is_valid():
            symptom_ids = serializer.validated_data['symptoms']
            symptoms = Symptom.objects.filter(id__in=symptom_ids)
            
            # Simple disease prediction logic (in real app, use ML model)
            diseases = Disease.objects.filter(symptoms__in=symptoms).distinct()
            
            # Create prediction record
            prediction = DiseasePrediction.objects.create(
                user=request.user,
                confidence_score=0.75  # Mock confidence
            )
            prediction.symptoms.set(symptoms)
            
            # Create prediction results
            for i, disease in enumerate(diseases[:5]):  # Top 5 predictions
                confidence = random.uniform(0.3, 0.9)
                DiseasePredictionResult.objects.create(
                    prediction=prediction,
                    disease=disease,
                    confidence=confidence,
                    rank=i+1
                )
            
            return Response({
                'prediction_id': prediction.id,
                'diseases': DiseaseSerializer(diseases[:5], many=True).data,
                'confidence_score': prediction.confidence_score
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Medicine Views
class MedicineListView(generics.ListAPIView):
    queryset = Medicine.objects.filter(is_active=True)
    serializer_class = MedicineSerializer
    permission_classes = [AllowAny]

class MedicineDetailView(generics.RetrieveAPIView):
    queryset = Medicine.objects.filter(is_active=True)
    serializer_class = MedicineSerializer
    permission_classes = [AllowAny]

class MedicineRecommendationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = MedicineRecommendationSerializer(data=request.data)
        if serializer.is_valid():
            disease_id = serializer.validated_data['disease_id']
            disease = get_object_or_404(Disease, id=disease_id)
            
            # Simple recommendation logic (in real app, use ML model)
            recommended_medicines = Medicine.objects.filter(
                is_active=True,
                prescription_required=False
            )[:10]
            
            return Response({
                'disease': DiseaseSerializer(disease).data,
                'recommended_medicines': MedicineSerializer(recommended_medicines, many=True).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Cart Views
class CartView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
            medicine = get_object_or_404(Medicine, id=serializer.validated_data['medicine_id'])
            quantity = serializer.validated_data['quantity']
            
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                medicine=medicine,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            return Response(CartSerializer(cart).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartItemView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        serializer = UpdateCartItemSerializer(data=request.data)
        if serializer.is_valid():
            cart_item.quantity = serializer.validated_data['quantity']
            cart_item.save()
            return Response(CartSerializer(cart_item.cart).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart = cart_item.cart
        cart_item.delete()
        return Response(CartSerializer(cart).data)

# Order Views
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            cart = get_object_or_404(Cart, user=request.user, is_active=True)
            cart_items = cart.cartitem_set.all()
            
            if not cart_items.exists():
                return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create order
            order = Order.objects.create(
                user=request.user,
                total_amount=cart.total_amount,
                shipping_address=serializer.validated_data['shipping_address'],
                phone=serializer.validated_data['phone'],
                payment_method=serializer.validated_data['payment_method']
            )
            
            # Create order items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    medicine=cart_item.medicine,
                    quantity=cart_item.quantity,
                    price=cart_item.medicine.price
                )
            
            # Clear cart
            cart.is_active = False
            cart.save()
            
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Chat Views
class ChatHistoryView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        session_id = self.request.query_params.get('session_id')
        if session_id:
            return ChatMessage.objects.filter(session_id=session_id, user=self.request.user)
        return ChatMessage.objects.filter(user=self.request.user).order_by('-timestamp')[:50]

class ChatBotView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.validated_data['message']
            session_id = serializer.validated_data.get('session_id', str(uuid.uuid4()))
            
            # Save user message
            ChatMessage.objects.create(
                session_id=session_id,
                message_type='USER',
                content=message,
                user=request.user
            )
            
            # Simple chatbot response (in real app, use NLP/AI)
            bot_response = self.generate_bot_response(message)
            
            # Save bot response
            ChatMessage.objects.create(
                session_id=session_id,
                message_type='BOT',
                content=bot_response,
                user=request.user
            )
            
            return Response({
                'session_id': session_id,
                'response': bot_response
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def generate_bot_response(self, message):
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! I'm your healthcare assistant. How can I help you today?"
        elif any(word in message_lower for word in ['symptom', 'pain', 'hurt']):
            return "I can help you check your symptoms. Please visit our symptom checker page for a detailed analysis."
        elif any(word in message_lower for word in ['medicine', 'drug', 'medication']):
            return "I can help you find medicines. Please visit our pharmacy section to browse available medications."
        elif any(word in message_lower for word in ['appointment', 'doctor', 'visit']):
            return "For appointments, please contact our support team or visit a nearby healthcare facility."
        else:
            return "I'm here to help with your healthcare needs. You can ask me about symptoms, medicines, or general health questions."

# Prescription Views
class PrescriptionListView(generics.ListAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Prescription.objects.filter(user=self.request.user).order_by('-prescribed_date')

class PrescriptionDetailView(generics.RetrieveAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Prescription.objects.filter(user=self.request.user)

# User Profile Views
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    
    def put(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Admin Views for Data Management
class AdminSymptomView(generics.ListCreateAPIView):
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminDiseaseView(generics.ListCreateAPIView):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminMedicineView(generics.ListCreateAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [permissions.IsAdminUser]

# Health Statistics
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def health_stats(request):
    user = request.user
    
    # Get user's health statistics
    total_predictions = DiseasePrediction.objects.filter(user=user).count()
    total_orders = Order.objects.filter(user=user).count()
    total_prescriptions = Prescription.objects.filter(user=user).count()
    
    return Response({
        'total_predictions': total_predictions,
        'total_orders': total_orders,
        'total_prescriptions': total_prescriptions,
        'last_prediction': DiseasePrediction.objects.filter(user=user).order_by('-created_at').first() is not None,
        'last_order': Order.objects.filter(user=user).order_by('-created_at').first() is not None,
    })
