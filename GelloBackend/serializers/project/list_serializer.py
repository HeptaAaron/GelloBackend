from rest_framework import serializers

from GelloBackend.models.project_models import Project


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "indicatorColor", "created_at", "updated_at"]