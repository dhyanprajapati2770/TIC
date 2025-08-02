from django.db import models
from symptoms.models import Symptom
from users.models import User


class Disease(models.Model):
    """Model for storing diseases."""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    symptoms = models.ManyToManyField(Symptom, related_name='diseases')
    severity_level = models.IntegerField(
        choices=[
            (1, 'Mild'),
            (2, 'Moderate'),
            (3, 'Severe'),
            (4, 'Critical'),
        ],
        default=1
    )
    category = models.CharField(
        max_length=50,
        choices=[
            ('infectious', 'Infectious Disease'),
            ('chronic', 'Chronic Disease'),
            ('genetic', 'Genetic Disorder'),
            ('autoimmune', 'Autoimmune Disease'),
            ('cancer', 'Cancer'),
            ('mental', 'Mental Health'),
            ('cardiovascular', 'Cardiovascular'),
            ('respiratory', 'Respiratory'),
            ('gastrointestinal', 'Gastrointestinal'),
            ('neurological', 'Neurological'),
            ('other', 'Other'),
        ],
        default='other'
    )
    treatment = models.TextField(blank=True, null=True)
    prevention = models.TextField(blank=True, null=True)
    risk_factors = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class DiseasePrediction(models.Model):
    """Model for storing disease predictions."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='disease_predictions')
    symptoms = models.ManyToManyField(Symptom, through='PredictionSymptom')
    predicted_diseases = models.ManyToManyField(Disease, through='PredictionDisease')
    confidence_score = models.FloatField(default=0.0)
    age = models.IntegerField()
    gender = models.CharField(
        max_length=10,
        choices=[
            ('M', 'Male'),
            ('F', 'Female'),
            ('O', 'Other'),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Disease prediction for {self.user.username} on {self.created_at.date()}"


class PredictionSymptom(models.Model):
    """Intermediate model for prediction symptoms."""
    prediction = models.ForeignKey(DiseasePrediction, on_delete=models.CASCADE)
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)
    severity = models.IntegerField(
        choices=[
            (1, 'Mild'),
            (2, 'Moderate'),
            (3, 'Severe'),
            (4, 'Critical'),
        ],
        default=1
    )
    
    class Meta:
        unique_together = ['prediction', 'symptom']
    
    def __str__(self):
        return f"{self.symptom.name} - {self.get_severity_display()}"


class PredictionDisease(models.Model):
    """Intermediate model for prediction diseases."""
    prediction = models.ForeignKey(DiseasePrediction, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    probability = models.FloatField(default=0.0)
    rank = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['prediction', 'disease']
        ordering = ['-probability']
    
    def __str__(self):
        return f"{self.disease.name} - {self.probability:.2%}"
