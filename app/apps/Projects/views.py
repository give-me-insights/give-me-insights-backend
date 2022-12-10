from rest_framework.generics import CreateAPIView

from .models import Project
from .serializers import ProjectCreateSerializer


class CreateProjectView(CreateAPIView):
    serializer_class = ProjectCreateSerializer
    queryset = Project.objects

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
