from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from DjangoBackend.processors import gel_image_processor
from DjangoBackend.services.gel_segmentation_service import GelSegmentationService


class GelAnalyzeView(APIView):
    gel_service = GelSegmentationService(
        model_folder="DjangoBackend/gel_models"
    )

    permission_classes = [IsAuthenticated]

    def post(self, request):
        image_file = request.FILES.get("image")

        if not image_file:
            return Response(
                {"error": "No image provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            image = gel_image_processor.convert_to_png(image_file)
            image = gel_image_processor.convert_to_grayscale(image)

            result = self.gel_service.analyze(image)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return HttpResponse(result, content_type="image/png")
