from django.db import models
from users.models import User


class Symptom(models.Model):
    """Model for storing symptoms."""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
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
            ('respiratory', 'Respiratory'),
            ('cardiovascular', 'Cardiovascular'),
            ('neurological', 'Neurological'),
            ('gastrointestinal', 'Gastrointestinal'),
            ('musculoskeletal', 'Musculoskeletal'),
            ('skin', 'Skin'),
            ('eye', 'Eye'),
            ('ear', 'Ear'),
            ('mental', 'Mental Health'),
            ('general', 'General'),
        ],
        default='general'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class SymptomCheck(models.Model):
    """Model for storing symptom checks performed by users."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='symptom_checks')
    symptoms = models.ManyToManyField(Symptom, through='SymptomCheckDetail')
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
        return f"Symptom check by {self.user.username} on {self.created_at.date()}"


class SymptomCheckDetail(models.Model):
    """Intermediate model for symptom check details."""
    symptom_check = models.ForeignKey(SymptomCheck, on_delete=models.CASCADE)
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
    duration_days = models.IntegerField(default=1)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ['symptom_check', 'symptom']
    
    def __str__(self):
        return f"{self.symptom.name} - {self.get_severity_display()}"
