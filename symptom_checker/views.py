from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Symptom, SymptomCheck, UserSymptom, SymptomAnalysis
from .serializers import (
    SymptomSerializer, SymptomCheckSerializer, 
    SymptomAnalysisSerializer, SymptomCheckCreateSerializer
)
import random
import json


class SymptomListView(generics.ListAPIView):
    """List all available symptoms"""
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Symptom.objects.all()
        category = self.request.query_params.get('category', None)
        search = self.request.query_params.get('search', None)
        
        if category:
            queryset = queryset.filter(category__icontains=category)
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        return queryset


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_symptom_check(request):
    """Submit a new symptom check"""
    serializer = SymptomCheckCreateSerializer(data=request.data)
    if serializer.is_valid():
        # Create symptom check
        symptom_check = SymptomCheck.objects.create(
            user=request.user,
            additional_info=serializer.validated_data.get('additional_info', ''),
            duration=serializer.validated_data.get('duration', '')
        )
        
        # Add symptoms with severity
        symptoms_data = serializer.validated_data['symptoms']
        for symptom_data in symptoms_data:
            UserSymptom.objects.create(
                symptom_check=symptom_check,
                symptom_id=symptom_data['symptom_id'],
                severity=symptom_data['severity'],
                notes=symptom_data.get('notes', '')
            )
        
        # Perform AI analysis
        analysis = perform_symptom_analysis(symptom_check)
        
        return Response({
            'message': 'Symptom check submitted successfully',
            'symptom_check': SymptomCheckSerializer(symptom_check).data,
            'analysis': SymptomAnalysisSerializer(analysis).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_symptom_history(request):
    """Get user's symptom check history"""
    symptom_checks = SymptomCheck.objects.filter(user=request.user)
    serializer = SymptomCheckSerializer(symptom_checks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_symptom_check_detail(request, check_id):
    """Get detailed information about a specific symptom check"""
    symptom_check = get_object_or_404(SymptomCheck, id=check_id, user=request.user)
    serializer = SymptomCheckSerializer(symptom_check)
    return Response(serializer.data)


def perform_symptom_analysis(symptom_check):
    """
    Perform AI analysis on symptom check
    This is a simplified version - in production, you'd use a trained ML model
    """
    user_symptoms = UserSymptom.objects.filter(symptom_check=symptom_check)
    
    # Simple rule-based analysis (replace with actual ML model)
    total_severity = sum([us.severity for us in user_symptoms])
    avg_severity = total_severity / len(user_symptoms) if user_symptoms else 0
    
    # Determine risk level based on symptoms and severity
    if avg_severity >= 4:
        risk_level = 'high'
        should_see_doctor = True
        urgency_level = 4
    elif avg_severity >= 3:
        risk_level = 'medium'
        should_see_doctor = True
        urgency_level = 3
    elif avg_severity >= 2:
        risk_level = 'medium'
        should_see_doctor = False
        urgency_level = 2
    else:
        risk_level = 'low'
        should_see_doctor = False
        urgency_level = 1
    
    # Generate possible conditions (simplified)
    possible_conditions = [
        {'condition': 'Common Cold', 'confidence': 0.7},
        {'condition': 'Flu', 'confidence': 0.5},
        {'condition': 'Allergic Reaction', 'confidence': 0.3}
    ]
    
    # Generate recommendations
    recommendations = generate_recommendations(risk_level, avg_severity, user_symptoms)
    
    # Create analysis record
    analysis = SymptomAnalysis.objects.create(
        symptom_check=symptom_check,
        risk_level=risk_level,
        possible_conditions=possible_conditions,
        recommendations=recommendations,
        should_see_doctor=should_see_doctor,
        urgency_level=urgency_level
    )
    
    return analysis


def generate_recommendations(risk_level, avg_severity, user_symptoms):
    """Generate recommendations based on analysis"""
    recommendations = []
    
    if risk_level == 'high':
        recommendations.append("Seek immediate medical attention")
        recommendations.append("Consider visiting an emergency room if symptoms worsen")
    elif risk_level == 'medium':
        recommendations.append("Schedule an appointment with your doctor within 24-48 hours")
        recommendations.append("Monitor symptoms closely")
    else:
        recommendations.append("Rest and stay hydrated")
        recommendations.append("Monitor symptoms and seek medical advice if they worsen")
    
    # Add symptom-specific recommendations
    symptom_names = [us.symptom.name.lower() for us in user_symptoms]
    
    if any('fever' in name for name in symptom_names):
        recommendations.append("Take temperature regularly and use fever reducers as needed")
    
    if any('cough' in name for name in symptom_names):
        recommendations.append("Stay hydrated and consider throat lozenges")
    
    if any('headache' in name for name in symptom_names):
        recommendations.append("Rest in a quiet, dark room")
    
    return '. '.join(recommendations)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_symptom_categories(request):
    """Get all symptom categories"""
    categories = Symptom.objects.values_list('category', flat=True).distinct()
    return Response(list(categories))