from rest_framework import serializers

from GelloBackend.models import Entry


class EntryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ["name", "description"]
        extra_kwargs = {
            "name": {"required": False},
            "description": {"required": False},
        }