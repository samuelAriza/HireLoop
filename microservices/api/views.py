# microservices/api/views.py
from rest_framework import generics
from microservices.models import MicroService
from .serializers import MicroServiceSerializer

class MicroServiceListAPIView(generics.ListAPIView):
    queryset = MicroService.objects.all()
    serializer_class = MicroServiceSerializer


class MicroServiceDetailAPIView(generics.RetrieveAPIView):
    queryset = MicroService.objects.all()
    serializer_class = MicroServiceSerializer
    lookup_field = "id"
