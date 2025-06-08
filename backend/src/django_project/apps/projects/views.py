from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Project
from .serializers import ProjectSerializer


class ProjectViewSet(UserPassesTestMixin, viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Admin users (staff) can see all projects
        if self.request.user.is_staff:
            return Project.objects.all()
        # Regular users can only see their own projects
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Ensure the owner is set to the current user for non-admin users
        if not self.request.user.is_staff:
            serializer.save(owner=self.request.user)
        else:
            # Admin can set owner explicitly if provided, otherwise set to themselves
            owner = serializer.validated_data.get('owner', self.request.user)
            serializer.save(owner=owner)

    def test_func(self):
        # This method is required by UserPassesTestMixin
        # Additional custom permission logic can be added here if needed
        return True
