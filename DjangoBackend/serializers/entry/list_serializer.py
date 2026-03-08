from rest_framework import serializers

from DjangoBackend.models import Entry


class EntryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ["id", "name", "type", "created_at", "updated_at" ]
        read_only_fields = ["id", "created_at", "updated_at" ]