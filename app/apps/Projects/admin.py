from django.contrib import admin
from .models import Project, DataSource, ProjectLink, Event, SourceDataSchemaMapping, SourceDataRowRaw


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("key", "title", "company", )


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ("key", "title", "project", "company", )


@admin.register(ProjectLink)
class ProjectLinkAdmin(admin.ModelAdmin):
    list_display = ("url", "title", "project", "company",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "company", "start_date", "duration", "duration_unit", )


@admin.register(SourceDataSchemaMapping)
class SourceDataSchemaMappingAdmin(admin.ModelAdmin):
    pass


@admin.register(SourceDataRowRaw)
class SourceDataRowRawAdmin(admin.ModelAdmin):
    list_filter = ("source", )
