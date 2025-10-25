from rest_framework import generics
from ..models import MicroService
from .serializers import MicroServiceSerializer

class MicroServiceListAPIView(generics.ListAPIView):
    """
    Retorna una lista JSON con todos los microservicios activos.
    """
    queryset = MicroService.objects.filter(is_active=True)
    serializer_class = MicroServiceSerializer

class MicroServiceDetailAPIView(generics.RetrieveAPIView):
    """
    Retorna un microservicio específico por su ID (UUID).
    """
    queryset = MicroService.objects.filter(is_active=True)
    serializer_class = MicroServiceSerializer
    lookup_field = "id"
