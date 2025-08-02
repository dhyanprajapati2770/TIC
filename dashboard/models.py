from django.db import models
from users.models import User
from symptoms.models import SymptomCheck
from diseases.models import DiseasePrediction
from pharmacy.models import Order


class UserActivity(models.Model):
    """Model for tracking user activities."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(
        max_length=50,
        choices=[
            ('login', 'Login'),
            ('symptom_check', 'Symptom Check'),
            ('disease_prediction', 'Disease Prediction'),
            ('medicine_search', 'Medicine Search'),
            ('chat_session', 'Chat Session'),
            ('order_placed', 'Order Placed'),
            ('profile_update', 'Profile Update'),
            ('other', 'Other'),
        ]
    )
    description = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'User activities'
    
    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()}"


class Analytics(models.Model):
    """Model for storing analytics data."""
    date = models.DateField(unique=True)
    total_users = models.IntegerField(default=0)
    active_users = models.IntegerField(default=0)
    symptom_checks = models.IntegerField(default=0)
    disease_predictions = models.IntegerField(default=0)
    chat_sessions = models.IntegerField(default=0)
    orders_placed = models.IntegerField(default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Analytics'
    
    def __str__(self):
        return f"Analytics for {self.date}"


class SystemHealth(models.Model):
    """Model for monitoring system health."""
    STATUS_CHOICES = [
        ('healthy', 'Healthy'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
        ('down', 'Down'),
    ]
    
    service_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    response_time = models.FloatField(help_text="Response time in milliseconds")
    error_count = models.IntegerField(default=0)
    last_check = models.DateTimeField(auto_now=True)
    details = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['service_name']
        verbose_name_plural = 'System health'
    
    def __str__(self):
        return f"{self.service_name} - {self.get_status_display()}"


class Notification(models.Model):
    """Model for system notifications."""
    NOTIFICATION_TYPE_CHOICES = [
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('alert', 'Alert'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES, default='info')
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} for {self.user.username}"
    
    def mark_as_read(self):
        from django.utils import timezone
        self.is_read = True
        self.read_at = timezone.now()
        self.save()


class UserReport(models.Model):
    """Model for user reports and feedback."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(
        max_length=50,
        choices=[
            ('bug', 'Bug Report'),
            ('feature_request', 'Feature Request'),
            ('feedback', 'Feedback'),
            ('complaint', 'Complaint'),
            ('suggestion', 'Suggestion'),
        ]
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('urgent', 'Urgent'),
        ],
        default='medium'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('open', 'Open'),
            ('in_progress', 'In Progress'),
            ('resolved', 'Resolved'),
            ('closed', 'Closed'),
        ],
        default='open'
    )
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='assigned_reports')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-priority', '-created_at']
    
    def __str__(self):
        return f"{self.title} by {self.user.username}"
