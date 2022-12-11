from rest_framework.permissions import IsAuthenticated

from .models import Project


class ProjectPermissions(IsAuthenticated):
    def has_permission(self, request, view):
        project = Project.objects.get(key=request.parser_context['kwargs']['project_key'])
        return super().has_permission(request, view) and request.user.company == project.company
