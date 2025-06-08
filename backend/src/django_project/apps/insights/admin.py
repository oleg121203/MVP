from django.contrib import admin
from .models import AIInsight

# Register your models here.

@admin.register(AIInsight)
class AIInsightAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'created_at', 'updated_at')
    list_filter = ('event_type', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
