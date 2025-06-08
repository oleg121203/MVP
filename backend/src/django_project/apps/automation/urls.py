from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AutomationRuleViewSet

router = DefaultRouter()
router.register(r'rules', AutomationRuleViewSet)

urlpatterns = [
    path('api/automation/', include(router.urls)),
]
