from rest_framework import serializers
from DjangoBackend.models.project_models import Project

class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "description", "indicatorColor", "created_at"]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        request = self.context["request"]
        return Project.objects.create(owner=request.user, **validated_data)