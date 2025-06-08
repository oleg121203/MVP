from django.db import models

# Create your models here.

class AIInsight(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    event_type = models.CharField(max_length=100, choices=[
        ('analysis', 'Analysis'),
        ('prediction', 'Prediction'),
        ('recommendation', 'Recommendation'),
        ('error', 'Error')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_event_type_display()}) - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
