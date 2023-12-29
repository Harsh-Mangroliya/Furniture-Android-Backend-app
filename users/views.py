from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from .models import user, CardDetail, otp
from rest_framework.views import APIView 
from .serializers import UserSerializer as userSerializer
from .serializers import CardDetailSerializer 
from django.conf import settings
from product.models import cart


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user_obj = user.objects.get(username=username)
            serializer = userSerializer(user_obj)
            if user_obj.check_password(password):
                return Response({
                    'msg': 'Login Successfull',
                    "user":serializer.data
                    }, status=status.HTTP_200_OK)
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
            try:
                serializer = userSerializer(data=request.data)
                if serializer.is_valid():
                    userObj = serializer.save()

                    #userObj = user.objects.get(email=request.data['email']) 
                    #print(userObj)        


                    
                    return Response({'msg': 'User Created'}, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)    
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
        

class CardDetailView(APIView):
    
    allowed_methods = ['GET', 'POST']

    def get(self, request,id = None):
        if id:
            try:
                card_obj = CardDetail.objects.filter(user=id)
                if not card_obj:
                    return Response({'msg': 'Card does not exist'}, status=status.HTTP_404_NOT_FOUND)
                
                serializer = CardDetailSerializer(card_obj, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            except Exception as e:
                return Response({'error': f'{e}'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'msg': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request,id = None):
        
        if id:
            card_obj = CardDetail.objects.filter(id=id)

            if card_obj:
                serializer = CardDetailSerializer(card_obj, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Card does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            serializer = CardDetailSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Card Created'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
