from rest_framework import serializers

from GelloBackend.models import Entry


class EntryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ["id", "project", "name", "content", "type", "created_at", "updated_at"]