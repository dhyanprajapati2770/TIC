from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    """Extended user model for healthcare application"""
    
    USER_TYPES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
        ('pharmacist', 'Pharmacist'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='patient')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.user_type})"


class UserProfile(models.Model):
    """Additional profile information for users"""
    
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    height = models.FloatField(help_text="Height in cm", blank=True, null=True)
    weight = models.FloatField(help_text="Weight in kg", blank=True, null=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    current_medications = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class DoctorProfile(models.Model):
    """Additional profile information for doctors"""
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    years_of_experience = models.PositiveIntegerField()
    qualification = models.TextField()
    clinic_address = models.TextField(blank=True, null=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    
    def __str__(self):
        return f"Dr. {self.user.username} - {self.specialization}"