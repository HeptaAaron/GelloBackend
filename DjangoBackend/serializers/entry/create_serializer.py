from rest_framework import serializers
from DjangoBackend.models import Entry


class EntryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ["id", "name", "content", "created_at"]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        project = self.context["project"]
        return Entry.objects.create(project=project, **validated_data)