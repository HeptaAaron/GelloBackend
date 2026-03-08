from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from DjangoBackend.models import Project, Entry
from DjangoBackend.serializers.entry.create_serializer import EntryCreateSerializer
from DjangoBackend.serializers.entry.list_serializer import EntryListSerializer
from DjangoBackend.serializers.entry.read_serializer import EntryReadSerializer
from DjangoBackend.serializers.entry.update_serializer import EntryUpdateSerializer


class EntryCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id : int):
        project = get_object_or_404(Project, id=project_id, owner=request.user)

        serializer = EntryCreateSerializer(data=request.data, context={'project': project})
        serializer.is_valid(raise_exception=True)
        entry = serializer.save()
        return Response(EntryCreateSerializer(entry).data, status=status.HTTP_201_CREATED)

class EntryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id : int):
        project = get_object_or_404(Project, id=project_id, owner=request.user)

        qs = Entry.objects.filter(project=project).order_by('-created_at')
        data = EntryListSerializer(qs, many=True).data
        return Response(data, status=status.HTTP_200_OK)

class EntryReadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id : int, entry_id : int):
        project = get_object_or_404(Project, id=project_id, owner=request.user)
        if project_id == 1:
            entry = get_object_or_404(Entry, id=entry_id, project=project)
            return Response(EntryReadSerializer(entry).data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

class EntryUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, project_id : int, entry_id : int):
        project = get_object_or_404(Project, id=project_id, owner=request.user)
        entry = get_object_or_404(Entry, id=entry_id, project=project)
        serializer = EntryUpdateSerializer(entry, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(EntryReadSerializer(entry).data, status=status.HTTP_200_OK)

class EntryDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, project_id : int, entry_id : int):
        project = get_object_or_404(Project, id=project_id, owner=request.user)
        entry = get_object_or_404(Entry, id=entry_id, project=project)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)