import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
from django.conf import settings
import logging

logger = logging.getLogger('healthcare')


class MedicineRecommenderModel:
    """Machine Learning model for medicine recommendation based on symptoms and conditions"""
    
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.similarity_model = None
        self.medicine_data = None
        self.is_trained = False
        self.model_path = os.path.join(settings.ML_MODELS_DIR, 'medicine_recommender.pkl')
    
    def create_sample_medicine_data(self):
        """Create sample medicine database"""
        medicines = [
            {
                'name': 'Paracetamol',
                'generic_name': 'Acetaminophen',
                'category': 'Analgesic',
                'indications': 'fever headache pain relief mild pain',
                'dosage': '500mg every 4-6 hours',
                'side_effects': 'nausea liver damage overdose',
                'contraindications': 'liver disease alcohol',
                'price': 5.99,
                'prescription_required': False
            },
            {
                'name': 'Ibuprofen',
                'generic_name': 'Ibuprofen',
                'category': 'NSAID',
                'indications': 'pain inflammation fever headache muscle pain',
                'dosage': '200-400mg every 4-6 hours',
                'side_effects': 'stomach upset bleeding kidney problems',
                'contraindications': 'kidney disease stomach ulcers',
                'price': 7.99,
                'prescription_required': False
            },
            {
                'name': 'Aspirin',
                'generic_name': 'Acetylsalicylic acid',
                'category': 'NSAID',
                'indications': 'pain fever inflammation heart protection',
                'dosage': '325-650mg every 4 hours',
                'side_effects': 'stomach bleeding tinnitus',
                'contraindications': 'children bleeding disorders',
                'price': 4.99,
                'prescription_required': False
            },
            {
                'name': 'Loratadine',
                'generic_name': 'Loratadine',
                'category': 'Antihistamine',
                'indications': 'allergies runny nose sneezing itching',
                'dosage': '10mg once daily',
                'side_effects': 'drowsiness dry mouth',
                'contraindications': 'severe liver disease',
                'price': 12.99,
                'prescription_required': False
            },
            {
                'name': 'Diphenhydramine',
                'generic_name': 'Diphenhydramine',
                'category': 'Antihistamine',
                'indications': 'allergies insomnia motion sickness',
                'dosage': '25-50mg every 4-6 hours',
                'side_effects': 'drowsiness dizziness dry mouth',
                'contraindications': 'glaucoma enlarged prostate',
                'price': 8.99,
                'prescription_required': False
            },
            {
                'name': 'Dextromethorphan',
                'generic_name': 'Dextromethorphan',
                'category': 'Cough Suppressant',
                'indications': 'dry cough persistent cough',
                'dosage': '15mg every 4 hours',
                'side_effects': 'dizziness nausea drowsiness',
                'contraindications': 'MAOI use respiratory depression',
                'price': 9.99,
                'prescription_required': False
            },
            {
                'name': 'Guaifenesin',
                'generic_name': 'Guaifenesin',
                'category': 'Expectorant',
                'indications': 'productive cough chest congestion',
                'dosage': '200-400mg every 4 hours',
                'side_effects': 'nausea vomiting dizziness',
                'contraindications': 'persistent cough',
                'price': 11.99,
                'prescription_required': False
            },
            {
                'name': 'Loperamide',
                'generic_name': 'Loperamide',
                'category': 'Antidiarrheal',
                'indications': 'diarrhea loose stools',
                'dosage': '2mg after each loose stool',
                'side_effects': 'constipation dizziness',
                'contraindications': 'bloody diarrhea fever',
                'price': 13.99,
                'prescription_required': False
            },
            {
                'name': 'Omeprazole',
                'generic_name': 'Omeprazole',
                'category': 'Proton Pump Inhibitor',
                'indications': 'heartburn acid reflux stomach ulcers',
                'dosage': '20mg once daily',
                'side_effects': 'headache nausea diarrhea',
                'contraindications': 'liver disease',
                'price': 15.99,
                'prescription_required': False
            },
            {
                'name': 'Simethicone',
                'generic_name': 'Simethicone',
                'category': 'Anti-gas',
                'indications': 'gas bloating abdominal discomfort',
                'dosage': '40-80mg after meals',
                'side_effects': 'minimal side effects',
                'contraindications': 'none known',
                'price': 6.99,
                'prescription_required': False
            }
        ]
        
        return pd.DataFrame(medicines)
    
    def train_model(self):
        """Train the medicine recommendation model"""
        logger.info("Training medicine recommendation model...")
        
        # Create medicine database
        self.medicine_data = self.create_sample_medicine_data()
        
        # Create combined text features for similarity matching
        self.medicine_data['combined_features'] = (
            self.medicine_data['indications'] + ' ' +
            self.medicine_data['category'] + ' ' +
            self.medicine_data['generic_name']
        )
        
        # Create TF-IDF matrix
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.medicine_data['combined_features'])
        
        # Compute similarity matrix
        self.similarity_matrix = cosine_similarity(tfidf_matrix)
        
        self.is_trained = True
        self.save_model()
        
        logger.info("Medicine recommendation model trained successfully")
        return True
    
    def recommend_medicines(self, symptoms_list, condition=None, max_recommendations=5):
        """
        Recommend medicines based on symptoms and/or condition
        symptoms_list: list of symptom names
        condition: diagnosed condition (optional)
        """
        if not self.is_trained:
            self.load_model()
        
        if not self.is_trained:
            logger.warning("Model not trained, training now...")
            self.train_model()
        
        # Create query text from symptoms and condition
        query_text = ' '.join(symptoms_list)
        if condition:
            query_text += ' ' + condition
        
        # Transform query to TF-IDF vector
        query_vector = self.tfidf_vectorizer.transform([query_text])
        
        # Compute similarities with all medicines
        medicine_features = self.tfidf_vectorizer.transform(self.medicine_data['combined_features'])
        similarities = cosine_similarity(query_vector, medicine_features).flatten()
        
        # Get top recommendations
        top_indices = similarities.argsort()[-max_recommendations:][::-1]
        
        recommendations = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Minimum similarity threshold
                medicine = self.medicine_data.iloc[idx]
                recommendations.append({
                    'name': medicine['name'],
                    'generic_name': medicine['generic_name'],
                    'category': medicine['category'],
                    'indications': medicine['indications'],
                    'dosage': medicine['dosage'],
                    'side_effects': medicine['side_effects'],
                    'contraindications': medicine['contraindications'],
                    'price': float(medicine['price']),
                    'prescription_required': medicine['prescription_required'],
                    'similarity_score': float(similarities[idx]),
                    'recommendation_reason': self._get_recommendation_reason(medicine, symptoms_list, condition)
                })
        
        return recommendations
    
    def _get_recommendation_reason(self, medicine, symptoms, condition):
        """Generate explanation for why this medicine was recommended"""
        reasons = []
        
        medicine_indications = medicine['indications'].lower().split()
        
        # Check symptom matches
        matching_symptoms = []
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            for indication in medicine_indications:
                if symptom_lower in indication or indication in symptom_lower:
                    matching_symptoms.append(symptom)
                    break
        
        if matching_symptoms:
            reasons.append(f"Effective for {', '.join(matching_symptoms)}")
        
        # Check condition match
        if condition and condition.lower() in medicine['indications'].lower():
            reasons.append(f"Commonly used for {condition}")
        
        # Add category information
        reasons.append(f"{medicine['category']} medication")
        
        return '; '.join(reasons) if reasons else "General symptom relief"
    
    def get_medicine_interactions(self, medicine_names):
        """
        Check for potential drug interactions (simplified)
        In production, this would use a comprehensive drug interaction database
        """
        interactions = []
        
        # Simple interaction rules (this should be expanded with real data)
        interaction_rules = {
            ('Aspirin', 'Ibuprofen'): 'Increased risk of bleeding and stomach problems',
            ('Paracetamol', 'alcohol'): 'Increased risk of liver damage',
            ('Diphenhydramine', 'alcohol'): 'Increased drowsiness and impairment'
        }
        
        for i, med1 in enumerate(medicine_names):
            for j, med2 in enumerate(medicine_names[i+1:], i+1):
                key = tuple(sorted([med1, med2]))
                if key in interaction_rules:
                    interactions.append({
                        'medicines': [med1, med2],
                        'interaction': interaction_rules[key],
                        'severity': 'moderate'
                    })
        
        return interactions
    
    def save_model(self):
        """Save the trained model to disk"""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        model_data = {
            'tfidf_vectorizer': self.tfidf_vectorizer,
            'medicine_data': self.medicine_data,
            'similarity_matrix': self.similarity_matrix,
            'is_trained': self.is_trained
        }
        
        joblib.dump(model_data, self.model_path)
        logger.info(f"Medicine recommender model saved to {self.model_path}")
    
    def load_model(self):
        """Load the trained model from disk"""
        if os.path.exists(self.model_path):
            try:
                model_data = joblib.load(self.model_path)
                self.tfidf_vectorizer = model_data['tfidf_vectorizer']
                self.medicine_data = model_data['medicine_data']
                self.similarity_matrix = model_data['similarity_matrix']
                self.is_trained = model_data['is_trained']
                logger.info("Medicine recommender model loaded successfully")
                return True
            except Exception as e:
                logger.error(f"Error loading medicine recommender model: {e}")
                return False
        return False


# Global instance
medicine_recommender = MedicineRecommenderModel()


def get_medicine_recommendations(symptoms_list, condition=None, max_recommendations=5):
    """
    Utility function to get medicine recommendations
    """
    return medicine_recommender.recommend_medicines(symptoms_list, condition, max_recommendations)


def check_medicine_interactions(medicine_names):
    """
    Utility function to check medicine interactions
    """
    return medicine_recommender.get_medicine_interactions(medicine_names)


def train_medicine_model():
    """Utility function to train the medicine recommendation model"""
    return medicine_recommender.train_model()