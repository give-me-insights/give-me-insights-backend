from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from .models import Project
from .serializers import ProjectSerializer


class ProjectListCreateView(ListCreateAPIView, RetrieveAPIView):
    lookup_field = "key"
    serializer_class = ProjectSerializer
    queryset = Project.objects

    def get_queryset(self):
        return self.queryset.filter(company=self.request.user.company).order_by("title")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get(self, request, *args, **kwargs):
        if "key" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)
