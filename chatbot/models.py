from django.db import models
from users.models import User


class ChatSession(models.Model):
    """Model for chat sessions."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    session_id = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Chat session {self.session_id} with {self.user.username}"


class ChatMessage(models.Model):
    """Model for chat messages."""
    MESSAGE_TYPE_CHOICES = [
        ('user', 'User'),
        ('bot', 'Bot'),
        ('system', 'System'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.get_message_type_display()} message at {self.timestamp}"


class BotResponse(models.Model):
    """Model for storing bot responses."""
    trigger_keywords = models.TextField(help_text="Comma-separated keywords that trigger this response")
    response_text = models.TextField()
    category = models.CharField(
        max_length=50,
        choices=[
            ('greeting', 'Greeting'),
            ('symptom_check', 'Symptom Check'),
            ('medicine_info', 'Medicine Information'),
            ('general_health', 'General Health'),
            ('emergency', 'Emergency'),
            ('appointment', 'Appointment'),
            ('faq', 'FAQ'),
            ('other', 'Other'),
        ],
        default='other'
    )
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-priority', 'category']
    
    def __str__(self):
        return f"{self.category}: {self.response_text[:50]}..."


class UserQuery(models.Model):
    """Model for storing user queries for analysis."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='queries')
    query_text = models.TextField()
    intent = models.CharField(max_length=100, blank=True, null=True)
    confidence = models.FloatField(default=0.0)
    entities = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'User queries'
    
    def __str__(self):
        return f"Query by {self.user.username}: {self.query_text[:50]}..."
