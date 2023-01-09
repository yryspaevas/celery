from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import RegisterSerializer


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=201)