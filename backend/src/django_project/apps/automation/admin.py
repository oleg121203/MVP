from django.contrib import admin
from .models import AutomationRule

# Register your models here.

@admin.register(AutomationRule)
class AutomationRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'trigger_type', 'action_type', 'is_active', 'created_at')
    list_filter = ('trigger_type', 'action_type', 'is_active')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
