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
        uploaded_image = request.FILES.get("image")

        if not uploaded_image:
            return Response(
                {"error": "No image provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            original_rgb = gel_image_processor.convert_to_png(uploaded_image)
            grayscale_for_analysis = gel_image_processor.convert_to_grayscale(original_rgb)

            analysis_result = self.gel_service.analyze(original_rgb, grayscale_for_analysis)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "image": analysis_result["image"],
                "processed-image": analysis_result["processed_image"],
                "lane-count": analysis_result["lane_count"],
                "table-data": analysis_result["table_data"],
                "note": analysis_result["note"],
            },
            status=status.HTTP_200_OK,
        )
