from rest_framework import serializers

from GelloBackend.models.project_models import Project
from GelloBackend.serializers.user.read_serializer import ReadSerializer


class ProjectListSerializer(serializers.ModelSerializer):
    entry_count = serializers.IntegerField(read_only=True)
    owner = ReadSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "indicatorColor", "owner", "entry_count", "created_at", "updated_at"]