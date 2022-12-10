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

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = generate_key(max_length=4)
        return super().save(*args, **kwargs)
