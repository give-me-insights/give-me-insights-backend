from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Project, DataSource, Event, ProjectLink, SourceDataRowRaw


User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "key", "title", "description", "timestamp", "last_change_timestamp", ]

    def create(self, validated_data, *args, **kwargs):
        user: User = validated_data.pop("user")
        return Project.objects.create(company=user.user.company, **validated_data)


class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = ("id", "key", "project", "title", "description", "timestamp", "inbound_topic",)
        extra_kwargs = {
            "project": {
                "read_only": True,
            },
        }


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "id",
            "key",
            "project",
            "title",
            "description",
            "timestamp",
            "start_date",
            "is_expected",
            "duration",
            "duration_unit",
        )
        extra_kwargs = {
            "project": {
                "read_only": True,
            },
        }


class ProjectLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectLink
        fields = ("id", "key", "project", "title", "description", "timestamp", "url",)
        extra_kwargs = {
            "project": {
                "read_only": True,
            },
        }
