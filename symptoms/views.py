from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Symptom, SymptomCheck, SymptomCheckDetail


def symptom_checker(request):
    """Symptom checker view."""
    symptoms = Symptom.objects.filter(is_active=True).order_by('category', 'name')
    return render(request, 'symptoms/symptom_checker.html', {'symptoms': symptoms})


@login_required
def check_symptoms(request):
    """Check symptoms view."""
    if request.method == 'POST':
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        selected_symptoms = request.POST.getlist('symptoms')
        severities = request.POST.getlist('severities')
        durations = request.POST.getlist('durations')
        
        if not age or not gender or not selected_symptoms:
            return JsonResponse({'error': 'Please fill all required fields'}, status=400)
        
        # Create symptom check
        symptom_check = SymptomCheck.objects.create(
            user=request.user,
            age=age,
            gender=gender
        )
        
        # Add symptoms to check
        for i, symptom_id in enumerate(selected_symptoms):
            try:
                symptom = Symptom.objects.get(id=symptom_id)
                severity = int(severities[i]) if i < len(severities) else 1
                duration = int(durations[i]) if i < len(durations) else 1
                
                SymptomCheckDetail.objects.create(
                    symptom_check=symptom_check,
                    symptom=symptom,
                    severity=severity,
                    duration_days=duration
                )
            except Symptom.DoesNotExist:
                continue
        
        return JsonResponse({
            'success': True,
            'check_id': symptom_check.id,
            'redirect_url': f'/api/diseases/predict/?check_id={symptom_check.id}'
        })
    
    return redirect('symptoms:symptom_checker')


@login_required
def symptom_history(request):
    """Symptom check history view."""
    checks = SymptomCheck.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'symptoms/symptom_history.html', {'checks': checks})


# API Views
@api_view(['GET'])
def symptom_list(request):
    """API endpoint for symptom list."""
    symptoms = Symptom.objects.filter(is_active=True).order_by('category', 'name')
    symptom_data = []
    
    for symptom in symptoms:
        symptom_data.append({
            'id': symptom.id,
            'name': symptom.name,
            'description': symptom.description,
            'category': symptom.category,
            'severity_level': symptom.severity_level,
        })
    
    return Response(symptom_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_check_symptoms(request):
    """API endpoint for symptom checking."""
    age = request.data.get('age')
    gender = request.data.get('gender')
    symptoms = request.data.get('symptoms', [])
    
    if not age or not gender or not symptoms:
        return Response({'error': 'Please provide age, gender, and symptoms'}, status=400)
    
    # Create symptom check
    symptom_check = SymptomCheck.objects.create(
        user=request.user,
        age=age,
        gender=gender
    )
    
    # Add symptoms to check
    for symptom_data in symptoms:
        try:
            symptom = Symptom.objects.get(id=symptom_data['id'])
            severity = symptom_data.get('severity', 1)
            duration = symptom_data.get('duration', 1)
            
            SymptomCheckDetail.objects.create(
                symptom_check=symptom_check,
                symptom=symptom,
                severity=severity,
                duration_days=duration
            )
        except Symptom.DoesNotExist:
            continue
    
    return Response({
        'success': True,
        'check_id': symptom_check.id,
        'message': 'Symptoms checked successfully'
    })
