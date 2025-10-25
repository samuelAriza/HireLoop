from rest_framework import serializers
from ..models import MicroService
from ..services.image_service import MicroserviceImageService

class MicroServiceSerializer(serializers.ModelSerializer):
    """Convierte los objetos MicroService en JSON"""

    freelancer_name = serializers.CharField(source='freelancer.user.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = MicroService
        fields = [
            'id',
            'title',
            'description',
            'price',
            'delivery_time',
            'category_name',
            'freelancer_name',
            'image_url',
        ]

    def get_image_url(self, obj):
        """Usa el servicio de imágenes para obtener la URL"""
        image_service = MicroserviceImageService()
        return image_service.get_image_url(obj.image_path)
