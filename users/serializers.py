from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = user
        fields = ['id','username','password','email','fullname','gender','DOB','phoneNo','is_active']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'write_only': True},
        }
        
    def create(self, validated_data):
        userobj = user(**validated_data)
        password = validated_data.pop('password', None)
        if password:
            userobj.set_password(password)
        userobj.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class CardDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardDetail
        fields = '__all__'
