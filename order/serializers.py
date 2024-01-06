from rest_framework import serializers
from .models import *

class orderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class orderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'

