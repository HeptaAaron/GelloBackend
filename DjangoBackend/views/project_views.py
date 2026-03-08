from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from DjangoBackend.models.project_models import Project
from DjangoBackend.serializers.project.create_serializer import ProjectCreateSerializer
from DjangoBackend.serializers.project.list_serializer import ProjectListSerializer
from DjangoBackend.serializers.project.read_serializer import ProjectReadSerializer
from DjangoBackend.serializers.project.update_serializer import ProjectUpdateSerializer


class ProjectCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProjectCreateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        project = serializer.save()
        return Response(ProjectCreateSerializer(project).data, status=status.HTTP_201_CREATED)

class ProjectListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Project.objects.filter(owner=request.user).annotate(entry_count=Count("entry")).order_by('-created_at')

        return Response(ProjectListSerializer(qs, many=True).data, status=status.HTTP_200_OK)

class ProjectReadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id: int):
        project = get_object_or_404(Project, id=id, owner=request.user)
        return Response(ProjectReadSerializer(project).data, status=status.HTTP_200_OK)

class ProjectUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, id: int):
        project = get_object_or_404(Project, id=id, owner=request.user)

        serializer = ProjectUpdateSerializer(project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(ProjectReadSerializer(project).data, status=status.HTTP_200_OK)

class ProjectDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id: int):
        project = get_object_or_404(Project, id=id, owner=request.user)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)