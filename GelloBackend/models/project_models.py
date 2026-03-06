from django.db import models
from django.conf import settings

class Project(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    indicatorColor = models.CharField(max_length=20, blank=False, default='#0000FF')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['owner', 'created_at']),
        ]

    def __str__(self):
        return f"{self.name} ({self.owner_id})"