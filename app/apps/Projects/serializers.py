from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Project

from apps.Account.serializers import CompanySerializer


User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "key", "title", "description", "timestamp", "last_change_timestamp", ]

    def create(self, validated_data, *args, **kwargs):
        user: User = validated_data.pop("user")
        return Project.objects.create(company=user.user.company, **validated_data)
