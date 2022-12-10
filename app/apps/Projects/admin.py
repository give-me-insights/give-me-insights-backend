from django.contrib import admin
from .models import Project, DataSource


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("key", "title", "company", )


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ("key", "title", "project", "company", )
