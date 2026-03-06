from rest_framework import serializers

from GelloBackend.models.project_models import Project


class ProjectReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "description", "indicatorColor", "created_at", "updated_at"]