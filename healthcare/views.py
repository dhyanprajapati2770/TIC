from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import HealthProfile, Appointment, HealthRecord, VitalSigns


def home(request):
    """Home page view."""
    return render(request, 'healthcare/home.html')


@login_required
def health_profile(request):
    """Health profile view."""
    profile, created = HealthProfile.objects.get_or_create(user=request.user)
    return render(request, 'healthcare/health_profile.html', {'profile': profile})


@login_required
def appointments(request):
    """Appointments view."""
    appointments = Appointment.objects.filter(user=request.user).order_by('-appointment_date')
    return render(request, 'healthcare/appointments.html', {'appointments': appointments})


@login_required
def health_records(request):
    """Health records view."""
    records = HealthRecord.objects.filter(user=request.user).order_by('-date')
    return render(request, 'healthcare/health_records.html', {'records': records})


@login_required
def vital_signs(request):
    """Vital signs view."""
    vital_signs = VitalSigns.objects.filter(user=request.user).order_by('-date')
    return render(request, 'healthcare/vital_signs.html', {'vital_signs': vital_signs})


# API Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_health_profile(request):
    """API endpoint for health profile."""
    profile, created = HealthProfile.objects.get_or_create(user=request.user)
    return Response({
        'height': profile.height,
        'weight': profile.weight,
        'bmi': profile.bmi,
        'allergies': profile.allergies,
        'medical_conditions': profile.medical_conditions,
        'current_medications': profile.current_medications,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_update_health_profile(request):
    """API endpoint to update health profile."""
    profile, created = HealthProfile.objects.get_or_create(user=request.user)
    
    if 'height' in request.data:
        profile.height = request.data['height']
    if 'weight' in request.data:
        profile.weight = request.data['weight']
    if 'allergies' in request.data:
        profile.allergies = request.data['allergies']
    if 'medical_conditions' in request.data:
        profile.medical_conditions = request.data['medical_conditions']
    if 'current_medications' in request.data:
        profile.current_medications = request.data['current_medications']
    
    profile.save()
    profile.calculate_bmi()
    
    return Response({'message': 'Health profile updated successfully'})
