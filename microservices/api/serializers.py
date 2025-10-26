from rest_framework import serializers
from microservices.models import MicroService

class MicroServiceSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = MicroService
        fields = [
            'id',
            'freelancer',
            'category',
            'title',
            'description',
            'price',
            'delivery_time',
            'is_active',
            'image_path',
            'created_at',
            'updated_at',
            'url',
        ]

    def get_url(self, obj):
        """Genera el link absoluto al detalle del microservicio"""
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f"/microservices/microservice/{obj.id}/")
        return f"/microservices/microservice/{obj.id}/"
