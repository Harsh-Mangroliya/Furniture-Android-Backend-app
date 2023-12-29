from rest_framework import serializers
from .models import *

class orderSerializer(serializers.ModelSerializer):
    class meta:
        model = Order
        field = '__all__'

class orderDetailSerializer(serializers.ModelSerializer):
    class meta:
        model = OrderDetail
        field = '__all__'

