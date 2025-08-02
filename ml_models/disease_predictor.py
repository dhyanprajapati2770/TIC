import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
from django.conf import settings
import logging

logger = logging.getLogger('healthcare')


class DiseasePredictorModel:
    """Machine Learning model for disease prediction based on symptoms"""
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.symptom_encoder = LabelEncoder()
        self.disease_encoder = LabelEncoder()
        self.is_trained = False
        self.model_path = os.path.join(settings.ML_MODELS_DIR, 'disease_predictor.pkl')
        self.encoders_path = os.path.join(settings.ML_MODELS_DIR, 'disease_encoders.pkl')
    
    def create_sample_data(self):
        """Create sample training data for the disease predictor"""
        # This is sample data - in production, you'd use real medical datasets
        symptoms = [
            'fever', 'cough', 'headache', 'fatigue', 'sore_throat', 'runny_nose',
            'body_aches', 'nausea', 'vomiting', 'diarrhea', 'chest_pain',
            'shortness_of_breath', 'dizziness', 'rash', 'abdominal_pain'
        ]
        
        diseases = [
            'Common Cold', 'Flu', 'COVID-19', 'Strep Throat', 'Gastroenteritis',
            'Migraine', 'Food Poisoning', 'Allergic Reaction', 'Pneumonia', 'Bronchitis'
        ]
        
        # Generate synthetic training data
        np.random.seed(42)
        data = []
        
        # Define symptom patterns for each disease
        disease_patterns = {
            'Common Cold': ['runny_nose', 'sore_throat', 'cough', 'headache'],
            'Flu': ['fever', 'body_aches', 'fatigue', 'headache', 'cough'],
            'COVID-19': ['fever', 'cough', 'fatigue', 'shortness_of_breath'],
            'Strep Throat': ['sore_throat', 'fever', 'headache'],
            'Gastroenteritis': ['nausea', 'vomiting', 'diarrhea', 'abdominal_pain'],
            'Migraine': ['headache', 'nausea', 'dizziness'],
            'Food Poisoning': ['nausea', 'vomiting', 'diarrhea', 'abdominal_pain'],
            'Allergic Reaction': ['rash', 'runny_nose', 'shortness_of_breath'],
            'Pneumonia': ['fever', 'cough', 'chest_pain', 'shortness_of_breath'],
            'Bronchitis': ['cough', 'chest_pain', 'fatigue']
        }
        
        for disease, primary_symptoms in disease_patterns.items():
            for _ in range(100):  # Generate 100 samples per disease
                sample = {symptom: 0 for symptom in symptoms}
                
                # Add primary symptoms with high probability
                for symptom in primary_symptoms:
                    if np.random.random() > 0.2:  # 80% chance
                        sample[symptom] = np.random.randint(3, 6)  # Severity 3-5
                
                # Add some random secondary symptoms
                for symptom in symptoms:
                    if symptom not in primary_symptoms and np.random.random() > 0.8:
                        sample[symptom] = np.random.randint(1, 4)  # Severity 1-3
                
                sample['disease'] = disease
                data.append(sample)
        
        return pd.DataFrame(data)
    
    def train_model(self):
        """Train the disease prediction model"""
        logger.info("Training disease prediction model...")
        
        # Create or load training data
        df = self.create_sample_data()
        
        # Prepare features and target
        feature_columns = [col for col in df.columns if col != 'disease']
        X = df[feature_columns]
        y = df['disease']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        logger.info(f"Model trained with accuracy: {accuracy:.2f}")
        
        # Save model and feature names
        self.feature_names = feature_columns
        self.is_trained = True
        self.save_model()
        
        return accuracy
    
    def predict_disease(self, symptoms_dict):
        """
        Predict disease based on symptoms
        symptoms_dict: {'symptom_name': severity_score, ...}
        """
        if not self.is_trained:
            self.load_model()
        
        if not self.is_trained:
            logger.warning("Model not trained, training now...")
            self.train_model()
        
        # Prepare input features
        features = np.zeros(len(self.feature_names))
        
        for i, feature in enumerate(self.feature_names):
            if feature in symptoms_dict:
                features[i] = symptoms_dict[feature]
        
        # Make prediction
        prediction = self.model.predict([features])[0]
        probabilities = self.model.predict_proba([features])[0]
        
        # Get top 3 predictions with confidence scores
        class_names = self.model.classes_
        predictions_with_confidence = [
            {
                'disease': class_names[i],
                'confidence': float(prob)
            }
            for i, prob in enumerate(probabilities)
        ]
        
        # Sort by confidence and return top 3
        predictions_with_confidence.sort(key=lambda x: x['confidence'], reverse=True)
        
        return {
            'primary_prediction': prediction,
            'all_predictions': predictions_with_confidence[:3]
        }
    
    def save_model(self):
        """Save the trained model to disk"""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        model_data = {
            'model': self.model,
            'feature_names': self.feature_names,
            'is_trained': self.is_trained
        }
        
        joblib.dump(model_data, self.model_path)
        logger.info(f"Model saved to {self.model_path}")
    
    def load_model(self):
        """Load the trained model from disk"""
        if os.path.exists(self.model_path):
            try:
                model_data = joblib.load(self.model_path)
                self.model = model_data['model']
                self.feature_names = model_data['feature_names']
                self.is_trained = model_data['is_trained']
                logger.info("Model loaded successfully")
                return True
            except Exception as e:
                logger.error(f"Error loading model: {e}")
                return False
        return False


# Global instance
disease_predictor = DiseasePredictorModel()


def get_disease_predictions(symptoms_dict):
    """
    Utility function to get disease predictions
    symptoms_dict: {'symptom_name': severity_score, ...}
    """
    return disease_predictor.predict_disease(symptoms_dict)


def train_disease_model():
    """Utility function to train the model"""
    return disease_predictor.train_model()