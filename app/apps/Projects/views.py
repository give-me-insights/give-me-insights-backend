from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, DestroyAPIView
from .models import Project, DataSource, Event, ProjectLink
from .serializers import ProjectSerializer, DataSourceSerializer, EventSerializer, ProjectLinkSerializer
from .permissions import ProjectPermissions
from rest_framework.generics import get_object_or_404


class ProjectListCreateRetrieveView(ListCreateAPIView, RetrieveAPIView):
    lookup_field = "key"
    serializer_class = ProjectSerializer
    queryset = Project.objects

    def get_queryset(self):
        return self.queryset.filter(company=self.request.user.company).order_by("title")

    def filter_queryset(self, queryset):
        return queryset.filter(company=self.request.user.company)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get(self, request, *args, **kwargs):
        if "key" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)


class PluginMixin:
    def perform_create(self, serializer):
        project = get_object_or_404(Project.objects, key=self.kwargs["project_key"])
        serializer.save(project=project)

    def filter_queryset(self, queryset):
        return queryset.filter(project__company=self.request.user.company)


class DataSourceListCreateView(PluginMixin, ListCreateAPIView, DestroyAPIView):
    lookup_field = "key"
    serializer_class = DataSourceSerializer
    queryset = DataSource.objects
    permission_classes = (ProjectPermissions, )


class EventListCreateView(PluginMixin, ListCreateAPIView, DestroyAPIView):
    lookup_field = "key"
    serializer_class = EventSerializer
    queryset = Event.objects
    permission_classes = (ProjectPermissions, )


class ProjectLinkListCreateView(PluginMixin, ListCreateAPIView, DestroyAPIView):
    lookup_field = "key"
    serializer_class = ProjectLinkSerializer
    queryset = ProjectLink.objects
    permission_classes = (ProjectPermissions, )
