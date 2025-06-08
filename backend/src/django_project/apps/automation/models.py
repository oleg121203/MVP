from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import JSONField

User = get_user_model()

class AutomationRule(models.Model):
    TRIGGER_CHOICES = [
        ('analysis_complete', 'Analysis Complete'),
        ('new_data', 'New Data Available'),
        ('time_based', 'Time Based'),
    ]
    
    ACTION_CHOICES = [
        ('create_task', 'Create Task'),
        ('send_notification', 'Send Notification'),
        ('run_script', 'Run Script'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    trigger_type = models.CharField(max_length=50, choices=TRIGGER_CHOICES)
    trigger_config = JSONField(default=dict)
    condition = models.TextField(blank=True)
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    action_config = JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_trigger_type_display()} → {self.get_action_type_display()})"

# Create your models here.
