from rest_framework.generics import ListCreateAPIView

from .models import Project
from .serializers import ProjectSerializer


class ProjectListCreateView(ListCreateAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects

    def get_queryset(self):
        return self.queryset.filter(company=self.request.user.company).order_by("title")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
