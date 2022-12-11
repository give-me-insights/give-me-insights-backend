from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, DestroyAPIView, ListAPIView
from .models import (
    Project,
    DataSource,
    Event,
    ProjectLink,
    SourceDataRowRaw,
    SourceDataSchemaMapping,
    GroupedSourceData,
)
from .serializers import (
    ProjectSerializer,
    DataSourceSerializer,
    EventSerializer,
    ProjectLinkSerializer,
)
from .permissions import ProjectPermissions
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
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
        return queryset.filter(project__company=self.request.user.company, project__key=self.kwargs["project_key"])


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


class SourceDataRawView(ListAPIView):
    lookup_field = "source__key"
    lookup_url_kwarg = "source"
    queryset = SourceDataRowRaw.objects
    permission_classes = (ProjectPermissions,)
    authentication_classes = (TokenAuthentication, SessionAuthentication, )

    def list(self, request, *args, **kwargs):
        columns = SourceDataSchemaMapping.objects.get(source__key=kwargs["source"]).mapping.values()
        queryset = self.filter_queryset(self.get_queryset())
        entities = [
            tuple([entity.timestamp.timestamp()] + list(entity.value.values()))
            for entity in queryset.all()
        ]
        return Response({
            "columns": ["timestamp"] + list(columns),
            "values": entities
        })


class GroupedSourceDataView(ListAPIView):
    queryset = GroupedSourceData.objects
    permission_classes = (ProjectPermissions,)
    authentication_classes = (TokenAuthentication, SessionAuthentication,)

    def list(self, request, *args, **kwargs):
        columns = SourceDataSchemaMapping.objects.get(source__key=kwargs["source_key"]).mapping
        inverted_dict = {value: key for key, value in columns.items()}
        filter_ = {
            "source__project__key": kwargs["project_key"],
            "source__key": kwargs["source_key"],
            "method": kwargs["group_by_method"],
            "by_key": inverted_dict[kwargs["group_by_key"]],
        }
        entities = []
        column_names = ["timestamp", kwargs["group_by_key"]]
        columns_set = False
        for entity in self.queryset.filter(**filter_).all():
            timestamp = entity.timestamp.timestamp()
            value_of_key = entity.values.pop("value_of_key")
            values = []
            for key, measurement in entity.values.items():
                if not columns_set:
                    if "mean" in key or "sum" in key:
                        try:
                            column_names.append(columns[key.replace("sum_", "").replace("mean_", "")])
                        except:
                            column_names.append(key)
                    else:
                        column_names.append(key)
                values.append(measurement)
            # it's correct!
            columns_set = True
            entities.append([timestamp, value_of_key] + values)

        return Response({
            "columns": column_names,
            "values": entities
        })
