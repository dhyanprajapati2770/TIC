from django.core.management.base import BaseCommand
from healthcare.models import Symptom, Disease, Medicine
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populate database with sample healthcare data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample symptoms...')
        
        # Create symptoms
        symptoms_data = [
            {'name': 'Fever', 'description': 'Elevated body temperature', 'severity_level': 2, 'category': 'General'},
            {'name': 'Headache', 'description': 'Pain in the head or upper neck', 'severity_level': 2, 'category': 'Neurological'},
            {'name': 'Cough', 'description': 'Sudden expulsion of air from the lungs', 'severity_level': 1, 'category': 'Respiratory'},
            {'name': 'Fatigue', 'description': 'Extreme tiredness', 'severity_level': 1, 'category': 'General'},
            {'name': 'Nausea', 'description': 'Feeling of sickness with an inclination to vomit', 'severity_level': 2, 'category': 'Digestive'},
            {'name': 'Chest Pain', 'description': 'Pain in the chest area', 'severity_level': 4, 'category': 'Cardiovascular'},
            {'name': 'Shortness of Breath', 'description': 'Difficulty breathing', 'severity_level': 3, 'category': 'Respiratory'},
            {'name': 'Dizziness', 'description': 'Sensation of spinning or lightheadedness', 'severity_level': 2, 'category': 'Neurological'},
            {'name': 'Joint Pain', 'description': 'Pain in joints', 'severity_level': 2, 'category': 'Musculoskeletal'},
            {'name': 'Rash', 'description': 'Area of irritated or swollen skin', 'severity_level': 1, 'category': 'Dermatological'},
        ]
        
        symptoms = []
        for symptom_data in symptoms_data:
            symptom, created = Symptom.objects.get_or_create(
                name=symptom_data['name'],
                defaults=symptom_data
            )
            symptoms.append(symptom)
            if created:
                self.stdout.write(f'Created symptom: {symptom.name}')
        
        self.stdout.write('Creating sample diseases...')
        
        # Create diseases
        diseases_data = [
            {
                'name': 'Common Cold',
                'description': 'A viral infectious disease of the upper respiratory tract',
                'risk_level': 'LOW',
                'treatment': 'Rest, hydration, over-the-counter medications',
                'prevention': 'Good hygiene, avoiding close contact with sick people'
            },
            {
                'name': 'Influenza',
                'description': 'A viral infection that attacks your respiratory system',
                'risk_level': 'MEDIUM',
                'treatment': 'Rest, fluids, antiviral medications if prescribed',
                'prevention': 'Annual flu vaccination, good hygiene'
            },
            {
                'name': 'Hypertension',
                'description': 'High blood pressure',
                'risk_level': 'HIGH',
                'treatment': 'Lifestyle changes, medication',
                'prevention': 'Healthy diet, regular exercise, stress management'
            },
            {
                'name': 'Diabetes Type 2',
                'description': 'A chronic condition affecting how your body metabolizes glucose',
                'risk_level': 'HIGH',
                'treatment': 'Diet, exercise, medication, insulin if needed',
                'prevention': 'Healthy lifestyle, regular check-ups'
            },
            {
                'name': 'Migraine',
                'description': 'A neurological condition characterized by severe headaches',
                'risk_level': 'MEDIUM',
                'treatment': 'Pain relievers, preventive medications',
                'prevention': 'Identifying triggers, stress management'
            }
        ]
        
        diseases = []
        for disease_data in diseases_data:
            disease, created = Disease.objects.get_or_create(
                name=disease_data['name'],
                defaults=disease_data
            )
            diseases.append(disease)
            if created:
                self.stdout.write(f'Created disease: {disease.name}')
        
        # Associate symptoms with diseases
        cold_symptoms = [symptoms[0], symptoms[2], symptoms[3]]  # Fever, Cough, Fatigue
        flu_symptoms = [symptoms[0], symptoms[2], symptoms[3], symptoms[6]]  # Fever, Cough, Fatigue, Shortness of Breath
        hypertension_symptoms = [symptoms[5], symptoms[7]]  # Chest Pain, Dizziness
        diabetes_symptoms = [symptoms[3], symptoms[7]]  # Fatigue, Dizziness
        migraine_symptoms = [symptoms[1], symptoms[7]]  # Headache, Dizziness
        
        disease_symptom_mapping = {
            diseases[0]: cold_symptoms,  # Common Cold
            diseases[1]: flu_symptoms,   # Influenza
            diseases[2]: hypertension_symptoms,  # Hypertension
            diseases[3]: diabetes_symptoms,  # Diabetes
            diseases[4]: migraine_symptoms,  # Migraine
        }
        
        for disease, symptom_list in disease_symptom_mapping.items():
            disease.symptoms.add(*symptom_list)
            self.stdout.write(f'Associated symptoms with {disease.name}')
        
        self.stdout.write('Creating sample medicines...')
        
        # Create medicines
        medicines_data = [
            {
                'name': 'Paracetamol',
                'generic_name': 'Acetaminophen',
                'description': 'Pain reliever and fever reducer',
                'dosage_form': 'TABLET',
                'strength': '500mg',
                'manufacturer': 'Generic Pharma',
                'price': Decimal('5.99'),
                'stock_quantity': 100,
                'prescription_required': False,
                'side_effects': 'Rare: allergic reactions',
                'uses': 'Fever, pain relief'
            },
            {
                'name': 'Ibuprofen',
                'generic_name': 'Ibuprofen',
                'description': 'Non-steroidal anti-inflammatory drug',
                'dosage_form': 'TABLET',
                'strength': '400mg',
                'manufacturer': 'Generic Pharma',
                'price': Decimal('7.99'),
                'stock_quantity': 80,
                'prescription_required': False,
                'side_effects': 'Stomach upset, heartburn',
                'uses': 'Pain, inflammation, fever'
            },
            {
                'name': 'Cough Syrup',
                'generic_name': 'Dextromethorphan',
                'description': 'Cough suppressant',
                'dosage_form': 'SYRUP',
                'strength': '15mg/5ml',
                'manufacturer': 'CoughCare',
                'price': Decimal('12.99'),
                'stock_quantity': 50,
                'prescription_required': False,
                'side_effects': 'Drowsiness, dizziness',
                'uses': 'Dry cough relief'
            },
            {
                'name': 'Vitamin C',
                'generic_name': 'Ascorbic Acid',
                'description': 'Vitamin C supplement',
                'dosage_form': 'TABLET',
                'strength': '1000mg',
                'manufacturer': 'HealthVit',
                'price': Decimal('15.99'),
                'stock_quantity': 200,
                'prescription_required': False,
                'side_effects': 'Diarrhea in high doses',
                'uses': 'Immune support, antioxidant'
            },
            {
                'name': 'Omeprazole',
                'generic_name': 'Omeprazole',
                'description': 'Proton pump inhibitor for acid reflux',
                'dosage_form': 'CAPSULE',
                'strength': '20mg',
                'manufacturer': 'AcidCare',
                'price': Decimal('25.99'),
                'stock_quantity': 60,
                'prescription_required': True,
                'side_effects': 'Headache, diarrhea',
                'uses': 'Acid reflux, ulcers'
            }
        ]
        
        for medicine_data in medicines_data:
            medicine, created = Medicine.objects.get_or_create(
                name=medicine_data['name'],
                defaults=medicine_data
            )
            if created:
                self.stdout.write(f'Created medicine: {medicine.name}')
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample data!'))