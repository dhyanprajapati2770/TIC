from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from symptoms.models import SymptomCheck
from .models import Disease, DiseasePrediction, PredictionSymptom, PredictionDisease
import random


def disease_predictor(request):
    """Disease predictor view."""
    return render(request, 'diseases/disease_predictor.html')


@login_required
def predict_disease(request):
    """Predict disease view."""
    check_id = request.GET.get('check_id')
    
    if not check_id:
        return redirect('symptoms:symptom_checker')
    
    try:
        symptom_check = SymptomCheck.objects.get(id=check_id, user=request.user)
    except SymptomCheck.DoesNotExist:
        return redirect('symptoms:symptom_checker')
    
    # Get symptoms from check
    symptoms = symptom_check.symptoms.all()
    
    # Simple disease prediction logic (placeholder for ML model)
    predicted_diseases = predict_diseases_from_symptoms(symptoms, symptom_check.age, symptom_check.gender)
    
    # Create disease prediction record
    prediction = DiseasePrediction.objects.create(
        user=request.user,
        age=symptom_check.age,
        gender=symptom_check.gender,
        confidence_score=predicted_diseases['confidence']
    )
    
    # Add symptoms to prediction
    for symptom in symptoms:
        detail = symptom_check.symptomcheckdetail_set.get(symptom=symptom)
        PredictionSymptom.objects.create(
            prediction=prediction,
            symptom=symptom,
            severity=detail.severity
        )
    
    # Add predicted diseases
    for i, disease_data in enumerate(predicted_diseases['diseases']):
        try:
            disease = Disease.objects.get(name=disease_data['name'])
            PredictionDisease.objects.create(
                prediction=prediction,
                disease=disease,
                probability=disease_data['probability'],
                rank=i + 1
            )
        except Disease.DoesNotExist:
            continue
    
    return redirect('diseases:disease_result', prediction_id=prediction.id)


@login_required
def disease_result(request, prediction_id):
    """Disease result view."""
    prediction = get_object_or_404(DiseasePrediction, id=prediction_id, user=request.user)
    predicted_diseases = prediction.predicted_diseases.all().order_by('predictiondisease__rank')
    
    return render(request, 'diseases/disease_result.html', {
        'prediction': prediction,
        'predicted_diseases': predicted_diseases
    })


@login_required
def prediction_history(request):
    """Prediction history view."""
    predictions = DiseasePrediction.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'diseases/prediction_history.html', {'predictions': predictions})


def predict_diseases_from_symptoms(symptoms, age, gender):
    """Simple disease prediction logic (placeholder for ML model)."""
    # This is a simplified prediction logic
    # In a real application, you would use a trained ML model
    
    diseases = Disease.objects.filter(is_active=True)
    predicted_diseases = []
    
    # Simple scoring based on symptom matches
    for disease in diseases:
        disease_symptoms = disease.symptoms.all()
        matching_symptoms = set(symptoms) & set(disease_symptoms)
        
        if matching_symptoms:
            # Calculate probability based on symptom matches
            match_ratio = len(matching_symptoms) / len(disease_symptoms) if disease_symptoms else 0
            probability = min(match_ratio * 0.8 + random.uniform(0, 0.2), 0.95)
            
            predicted_diseases.append({
                'name': disease.name,
                'probability': probability,
                'description': disease.description,
                'treatment': disease.treatment
            })
    
    # Sort by probability and take top 5
    predicted_diseases.sort(key=lambda x: x['probability'], reverse=True)
    predicted_diseases = predicted_diseases[:5]
    
    # Calculate overall confidence
    confidence = sum(d['probability'] for d in predicted_diseases) / len(predicted_diseases) if predicted_diseases else 0
    
    return {
        'diseases': predicted_diseases,
        'confidence': confidence
    }


# API Views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_predict_disease(request):
    """API endpoint for disease prediction."""
    check_id = request.data.get('check_id')
    
    if not check_id:
        return Response({'error': 'Check ID is required'}, status=400)
    
    try:
        symptom_check = SymptomCheck.objects.get(id=check_id, user=request.user)
    except SymptomCheck.DoesNotExist:
        return Response({'error': 'Symptom check not found'}, status=400)
    
    # Get symptoms from check
    symptoms = symptom_check.symptoms.all()
    
    # Predict diseases
    prediction_result = predict_diseases_from_symptoms(symptoms, symptom_check.age, symptom_check.gender)
    
    # Create disease prediction record
    prediction = DiseasePrediction.objects.create(
        user=request.user,
        age=symptom_check.age,
        gender=symptom_check.gender,
        confidence_score=prediction_result['confidence']
    )
    
    # Add symptoms to prediction
    for symptom in symptoms:
        detail = symptom_check.symptomcheckdetail_set.get(symptom=symptom)
        PredictionSymptom.objects.create(
            prediction=prediction,
            symptom=symptom,
            severity=detail.severity
        )
    
    # Add predicted diseases
    for i, disease_data in enumerate(prediction_result['diseases']):
        try:
            disease = Disease.objects.get(name=disease_data['name'])
            PredictionDisease.objects.create(
                prediction=prediction,
                disease=disease,
                probability=disease_data['probability'],
                rank=i + 1
            )
        except Disease.DoesNotExist:
            continue
    
    return Response({
        'success': True,
        'prediction_id': prediction.id,
        'predicted_diseases': prediction_result['diseases'],
        'confidence': prediction_result['confidence']
    })
