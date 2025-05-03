from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class MyAPIView(APIView):
    def get(self, request):
        data = {"message": "Hello, world!"}
        return Response(data)

    def post(self, request):
        # Handle POST request
        return Response(status=status.HTTP_201_CREATED)
