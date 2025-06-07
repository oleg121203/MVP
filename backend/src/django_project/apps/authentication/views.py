import secrets

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer

# Create your views here.


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Додаткові дії при реєстрації
        refresh = RefreshToken.for_user(user)
        user.profile.verification_token = secrets.token_urlsafe(32)
        user.profile.save()

        # Відправка email для верифікації
        send_mail(
            "Verify your email",
            f"Please verify your email: {settings.BASE_URL}/verify/{user.profile.verification_token}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return Response(
            {
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )


class PasswordResetView(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response(
                {"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            token = secrets.token_urlsafe(32)
            user.auth_token = token
            user.save()

            reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"
            send_mail(
                "Відновлення пароля",
                f"Для відновлення пароля перейдіть за посиланням: {reset_link}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return Response(
                {"message": "Інструкції відправлено на email"},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {"error": "Користувача з таким email не знайдено"},
                status=status.HTTP_404_NOT_FOUND,
            )
