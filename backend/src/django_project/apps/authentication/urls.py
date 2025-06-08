from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from .views import PasswordResetView, RegisterView, DashboardCustomizationView, UserProfileView

urlpatterns = [
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("register/", RegisterView.as_view(), name="register"),
    path("password-reset/", PasswordResetView.as_view(), name="password_reset"),
    path("dashboard-customization/", DashboardCustomizationView.as_view(), name="dashboard_customization"),
    path('me/', UserProfileView.as_view(), name='user-profile'),
]
