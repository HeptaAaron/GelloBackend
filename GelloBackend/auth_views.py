from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        resp = super().post(request, *args, **kwargs)
        if resp.status_code != 200:
            return resp
        return Response(
            {
                "accessToken": resp.data["access"],
                "refreshToken": resp.data["refresh"],
            },
            status=status.HTTP_200_OK,
        )