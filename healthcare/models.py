from django.db import models
from users.models import User


class HealthProfile(models.Model):
    """Model for user health profiles."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='health_profile')
    height = models.DecimalField(max_digits=5, decimal_places=2, help_text="Height in cm", blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg", blank=True, null=True)
    bmi = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    medical_conditions = models.TextField(blank=True, null=True)
    current_medications = models.TextField(blank=True, null=True)
    family_history = models.TextField(blank=True, null=True)
    lifestyle_factors = models.JSONField(default=dict, blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Health profile for {self.user.username}"
    
    def calculate_bmi(self):
        if self.height and self.weight:
            height_m = self.height / 100
            self.bmi = self.weight / (height_m ** 2)
            self.save()
        return self.bmi


class Appointment(models.Model):
    """Model for medical appointments."""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments', limit_choices_to={'is_doctor': True})
    appointment_date = models.DateTimeField()
    duration_minutes = models.IntegerField(default=30)
    reason = models.TextField()
    symptoms = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-appointment_date']
    
    def __str__(self):
        return f"Appointment with Dr. {self.doctor.last_name} on {self.appointment_date.date()}"


class HealthRecord(models.Model):
    """Model for health records."""
    RECORD_TYPE_CHOICES = [
        ('vital_signs', 'Vital Signs'),
        ('lab_result', 'Lab Result'),
        ('diagnosis', 'Diagnosis'),
        ('treatment', 'Treatment'),
        ('medication', 'Medication'),
        ('vaccination', 'Vaccination'),
        ('surgery', 'Surgery'),
        ('allergy', 'Allergy'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_records')
    record_type = models.CharField(max_length=20, choices=RECORD_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='created_records', limit_choices_to={'is_doctor': True})
    attachments = models.JSONField(default=list, blank=True)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.title} for {self.user.username}"


class VitalSigns(models.Model):
    """Model for vital signs tracking."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vital_signs')
    date = models.DateField()
    temperature = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, help_text="Temperature in Celsius")
    blood_pressure_systolic = models.IntegerField(blank=True, null=True)
    blood_pressure_diastolic = models.IntegerField(blank=True, null=True)
    heart_rate = models.IntegerField(blank=True, null=True, help_text="Heart rate in BPM")
    respiratory_rate = models.IntegerField(blank=True, null=True, help_text="Respiratory rate in breaths per minute")
    oxygen_saturation = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, help_text="Oxygen saturation percentage")
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Weight in kg")
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Height in cm")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Vital signs'
    
    def __str__(self):
        return f"Vital signs for {self.user.username} on {self.date}"
    
    @property
    def bmi(self):
        if self.height and self.weight:
            height_m = self.height / 100
            return self.weight / (height_m ** 2)
        return None
