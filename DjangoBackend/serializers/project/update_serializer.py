from rest_framework import serializers

from GelloBackend.models.project_models import Project


class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "description", "indicatorColor"]
        extra_kwargs = {
            "name": {"required": False},
            "description": {"required": False},
            "indicatorColor": {"required": False},
        }