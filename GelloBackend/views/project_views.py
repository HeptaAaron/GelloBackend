from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from GelloBackend.models.project_models import Project
from GelloBackend.serializers.project.create_serializer import ProjectCreateSerializer
from GelloBackend.serializers.project.list_serializer import ProjectListSerializer
from GelloBackend.serializers.project.read_serializer import ProjectReadSerializer
from GelloBackend.serializers.project.update_serializer import ProjectUpdateSerializer


class ProjectCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProjectCreateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        project = serializer.save()
        return Response(ProjectCreateSerializer(project).data, status=status.HTTP_201_CREATED)

class ProjectListView(APIView):
    def get(self, request):
        qs = Project.objects.filter(owner=request.user).order_by('-created_at')
        return Response(ProjectListSerializer(qs, many=True).data)

class ProjectReadView(APIView):
    def get(self, request, id: int):
        project = get_object_or_404(Project, id=id, owner=request.user)
        return Response(ProjectReadSerializer(project).data)

class ProjectUpdateView(APIView):
    def patch(self, request, id: int):
        project = get_object_or_404(Project, id=id, owner=request.user)

        serializer = ProjectUpdateSerializer(project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(ProjectReadSerializer(project).data, status=status.HTTP_200_OK)

class ProjectDeleteView(APIView):
    def delete(self, request, id: int):
        project = get_object_or_404(Project, id=id, owner=request.user)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)