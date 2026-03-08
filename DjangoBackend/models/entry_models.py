from django.db import models

from GelloBackend.models import Project


class Entry(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    content = models.JSONField(default=dict, blank=True)
    type = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['project', 'created_at']),
        ]

    def __str__(self):
        return f"({self.project}/{self.name}"