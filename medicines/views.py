from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Medicine, MedicineRecommendation, MedicineCategory


def medicine_search(request):
    """Medicine search view."""
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    
    medicines = Medicine.objects.filter(is_active=True)
    
    if query:
        medicines = medicines.filter(name__icontains=query)
    
    if category:
        medicines = medicines.filter(categories__name=category)
    
    categories = MedicineCategory.objects.filter(is_active=True)
    
    return render(request, 'medicines/medicine_search.html', {
        'medicines': medicines,
        'categories': categories,
        'query': query,
        'selected_category': category
    })


@login_required
def medicine_recommendations(request):
    """Medicine recommendations view."""
    # Get user's recent symptoms or diseases for recommendations
    recommendations = MedicineRecommendation.objects.filter(is_active=True).order_by('-effectiveness_score')
    
    return render(request, 'medicines/medicine_recommendations.html', {
        'recommendations': recommendations
    })


def medicine_detail(request, medicine_id):
    """Medicine detail view."""
    medicine = get_object_or_404(Medicine, id=medicine_id, is_active=True)
    recommendations = MedicineRecommendation.objects.filter(medicine=medicine, is_active=True)
    
    return render(request, 'medicines/medicine_detail.html', {
        'medicine': medicine,
        'recommendations': recommendations
    })


# API Views
@api_view(['GET'])
def api_medicine_search(request):
    """API endpoint for medicine search."""
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    
    medicines = Medicine.objects.filter(is_active=True)
    
    if query:
        medicines = medicines.filter(name__icontains=query)
    
    if category:
        medicines = medicines.filter(categories__name=category)
    
    medicine_data = []
    for medicine in medicines:
        medicine_data.append({
            'id': medicine.id,
            'name': medicine.name,
            'generic_name': medicine.generic_name,
            'description': medicine.description,
            'dosage_form': medicine.dosage_form,
            'strength': medicine.strength,
            'manufacturer': medicine.manufacturer,
            'prescription_required': medicine.prescription_required,
            'price': str(medicine.price),
            'stock_quantity': medicine.stock_quantity,
        })
    
    return Response(medicine_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_medicine_recommendations(request):
    """API endpoint for medicine recommendations."""
    disease_id = request.GET.get('disease_id')
    symptom_id = request.GET.get('symptom_id')
    
    recommendations = MedicineRecommendation.objects.filter(is_active=True)
    
    if disease_id:
        recommendations = recommendations.filter(disease_id=disease_id)
    
    if symptom_id:
        recommendations = recommendations.filter(symptom_id=symptom_id)
    
    recommendations = recommendations.order_by('-effectiveness_score')
    
    recommendation_data = []
    for rec in recommendations:
        recommendation_data.append({
            'id': rec.id,
            'medicine_name': rec.medicine.name,
            'medicine_id': rec.medicine.id,
            'dosage': rec.dosage,
            'duration': rec.duration,
            'side_effects': rec.side_effects,
            'contraindications': rec.contraindications,
            'effectiveness_score': rec.effectiveness_score,
        })
    
    return Response(recommendation_data)


@api_view(['GET'])
def api_medicine_detail(request, medicine_id):
    """API endpoint for medicine detail."""
    try:
        medicine = Medicine.objects.get(id=medicine_id, is_active=True)
        
        medicine_data = {
            'id': medicine.id,
            'name': medicine.name,
            'generic_name': medicine.generic_name,
            'description': medicine.description,
            'dosage_form': medicine.dosage_form,
            'strength': medicine.strength,
            'manufacturer': medicine.manufacturer,
            'prescription_required': medicine.prescription_required,
            'price': str(medicine.price),
            'stock_quantity': medicine.stock_quantity,
            'treats_diseases': [d.name for d in medicine.treats_diseases.all()],
            'treats_symptoms': [s.name for s in medicine.treats_symptoms.all()],
        }
        
        return Response(medicine_data)
    except Medicine.DoesNotExist:
        return Response({'error': 'Medicine not found'}, status=404)
