from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = productImage
        fields = '__all__'
    
    def get_image_url(self, obj):
        return obj.image_url()

class cartSetializer(serializers.ModelSerializer):
    class Meta:
        model = cart
        fields = '__all__'
    