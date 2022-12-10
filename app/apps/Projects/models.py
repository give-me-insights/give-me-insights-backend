from django.db import models
from utils import generate_key


class Project(models.Model):
    key = models.CharField(
        max_length=4,
        unique=True,
        editable=False,
    )
    title = models.CharField(
        max_length=80,
    )
    description = models.TextField(
        blank=True,
    )
    company = models.ForeignKey(
        to="Account.Company",
        on_delete=models.CASCADE,
        related_name="projects",
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )
    last_change_timestamp = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        unique_together = ('key', 'company', )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = generate_key(max_length=4)
        return super().save(*args, **kwargs)


class DataSource(models.Model):
    key = models.CharField(
        max_length=6,
        unique=True,
        editable=False,
    )
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name="sources",
    )
    title = models.CharField(
        max_length=128,
    )
    description = models.TextField(
        blank=True,
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = ('key', 'project', )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = generate_key(max_length=6)
        return super().save(*args, **kwargs)

    @property
    def company(self):
        return self.project.company

    @property
    def inbound_topic(self):
        return f"DIT--{self.project.company.key}--{self.project.key}--{self.key}"
