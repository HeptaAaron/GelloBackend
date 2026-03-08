from rest_framework import serializers

from DjangoBackend.models import Entry


class EntryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ["name", "content", "type"]
        extra_kwargs = {
            "name": {"required": False},
            "description": {"required": False},
        }