from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Symptom(models.Model):
    """Model for storing symptoms"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50)  # e.g., 'respiratory', 'digestive', etc.
    severity_scale = models.CharField(max_length=20, default='1-10')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['category', 'name']


class SymptomCheck(models.Model):
    """Model for storing user symptom checks"""
    
    SEVERITY_CHOICES = (
        (1, 'Very Mild'),
        (2, 'Mild'),
        (3, 'Moderate'),
        (4, 'Severe'),
        (5, 'Very Severe'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='symptom_checks')
    symptoms = models.ManyToManyField(Symptom, through='UserSymptom')
    additional_info = models.TextField(blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)  # e.g., '2 days', '1 week'
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['-created_at']


class UserSymptom(models.Model):
    """Through model for SymptomCheck and Symptom with additional fields"""
    
    SEVERITY_CHOICES = (
        (1, 'Very Mild'),
        (2, 'Mild'),
        (3, 'Moderate'),
        (4, 'Severe'),
        (5, 'Very Severe'),
    )
    
    symptom_check = models.ForeignKey(SymptomCheck, on_delete=models.CASCADE)
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)
    severity = models.IntegerField(choices=SEVERITY_CHOICES)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.symptom.name} - Severity: {self.severity}"
    
    class Meta:
        unique_together = ('symptom_check', 'symptom')


class SymptomAnalysis(models.Model):
    """Model for storing AI analysis results"""
    
    RISK_LEVELS = (
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
        ('emergency', 'Emergency'),
    )
    
    symptom_check = models.OneToOneField(SymptomCheck, on_delete=models.CASCADE, related_name='analysis')
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS)
    possible_conditions = models.JSONField(default=list)  # List of possible conditions with confidence scores
    recommendations = models.TextField()
    should_see_doctor = models.BooleanField(default=False)
    urgency_level = models.IntegerField(default=1)  # 1-5 scale
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Analysis for {self.symptom_check.user.username} - {self.risk_level}"
    
    class Meta:
        ordering = ['-created_at']