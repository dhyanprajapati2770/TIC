from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class ChatRoom(models.Model):
    """General chat rooms"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Message(models.Model):
    """Messages in chat rooms"""
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        username = self.user.username if self.user else 'Anonymous'
        return f"{username}: {self.content[:50]}..."
    
    class Meta:
        ordering = ['timestamp']


class Consultation(models.Model):
    """Doctor-patient consultations"""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    CONSULTATION_TYPE_CHOICES = (
        ('general', 'General Consultation'),
        ('follow_up', 'Follow-up'),
        ('emergency', 'Emergency'),
        ('second_opinion', 'Second Opinion'),
    )
    
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_consultations')
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='doctor_consultations')
    
    consultation_type = models.CharField(max_length=20, choices=CONSULTATION_TYPE_CHOICES, default='general')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Consultation details
    chief_complaint = models.TextField(blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    
    # Medical information
    diagnosis = models.TextField(blank=True, null=True)
    treatment_plan = models.TextField(blank=True, null=True)
    prescribed_medicines = models.TextField(blank=True, null=True)
    follow_up_instructions = models.TextField(blank=True, null=True)
    
    # Consultation metadata
    started_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Rating and feedback
    patient_rating = models.IntegerField(blank=True, null=True, choices=[(i, i) for i in range(1, 6)])
    patient_feedback = models.TextField(blank=True, null=True)
    doctor_notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        doctor_name = self.doctor.username if self.doctor else 'Unassigned'
        return f"Consultation: {self.patient.username} - {doctor_name}"
    
    @property
    def duration_minutes(self):
        """Calculate consultation duration in minutes"""
        if self.started_at and self.ended_at:
            delta = self.ended_at - self.started_at
            return int(delta.total_seconds() / 60)
        return 0
    
    class Meta:
        ordering = ['-created_at']


class ConsultationMessage(models.Model):
    """Messages within a consultation"""
    
    MESSAGE_TYPE_CHOICES = (
        ('text', 'Text Message'),
        ('image', 'Image'),
        ('file', 'File'),
        ('prescription', 'Prescription'),
        ('ai_response', 'AI Response'),
    )
    
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default='text')
    content = models.TextField()
    
    # File attachments
    image = models.ImageField(upload_to='consultation_images/', blank=True, null=True)
    file = models.FileField(upload_to='consultation_files/', blank=True, null=True)
    
    # Message metadata
    is_ai_generated = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}..."
    
    class Meta:
        ordering = ['timestamp']


class DoctorAvailability(models.Model):
    """Doctor availability schedule"""
    
    WEEKDAY_CHOICES = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availability_schedule')
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    
    # Break times
    break_start = models.TimeField(blank=True, null=True)
    break_end = models.TimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        day_name = dict(self.WEEKDAY_CHOICES)[self.weekday]
        return f"Dr. {self.doctor.username} - {day_name} ({self.start_time}-{self.end_time})"
    
    class Meta:
        unique_together = ('doctor', 'weekday')
        ordering = ['doctor', 'weekday', 'start_time']


class ConsultationFeedback(models.Model):
    """Feedback for consultations"""
    
    consultation = models.OneToOneField(Consultation, on_delete=models.CASCADE, related_name='feedback')
    
    # Ratings (1-5 scale)
    overall_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    doctor_communication = models.IntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    wait_time_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    platform_ease = models.IntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    
    # Text feedback
    positive_feedback = models.TextField(blank=True, null=True)
    improvement_suggestions = models.TextField(blank=True, null=True)
    additional_comments = models.TextField(blank=True, null=True)
    
    # Recommendation
    would_recommend = models.BooleanField(default=True)
    would_consult_again = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Feedback for {self.consultation} - {self.overall_rating} stars"
    
    class Meta:
        ordering = ['-created_at']