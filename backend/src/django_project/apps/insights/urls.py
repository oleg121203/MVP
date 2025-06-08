from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AIInsightViewSet

router = DefaultRouter()
router.register(r'insights', AIInsightViewSet)

urlpatterns = [
    path('api/ai/', include(router.urls)),
]
