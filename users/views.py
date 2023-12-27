from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from .models import user
from rest_framework.views import APIView 
from .serializers import UserSerializer as userSerializer

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user_obj = user.objects.get(username=username)
            if user_obj.check_password(password):
                return Response({'msg': 'Login Successfull'}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Invalid Password'}, status=status.HTTP_401_UNAUTHORIZED)
        except user.DoesNotExist:
            return Response({'msg': 'User does not exist'}, status=status.HTTP_401_UNAUTHORIZED)

class UserView(APIView):

    allowed_methods = ['GET', 'POST', 'PATCH']

    def get(self, request,id = None):
        if id:
            try:
                user_obj = user.objects.get(id=id)
                serializer = userSerializer(user_obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except user.DoesNotExist:
                return Response({'msg': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            users = user.objects.all()
            serializer = userSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request,id = None):
        if id:
            return Response({'msg': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = userSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'User Created'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    def patch(self, request,id = None):
        if id:
            try:
                user_obj = user.objects.get(id=id)
                serializer = userSerializer(user_obj, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'msg': 'User Updated'}, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except user.DoesNotExist:
                return Response({'msg': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'msg': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)