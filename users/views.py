from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from .models import user, CardDetail, otp
from rest_framework.views import APIView 
from .serializers import UserSerializer as userSerializer
from .serializers import CardDetailSerializer 
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import async_to_sync


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
        

class CardDetailView(APIView):
    
    allowed_methods = ['GET', 'POST']

    def get(self, request,id = None):
        if id:
            try:
                
                card_obj = CardDetail.objects.filter(user=id)
                if not card_obj:
                    return Response({'msg': 'Card does not exist'}, status=status.HTTP_404_NOT_FOUND)
                
                serializer = CardDetailSerializer(card_obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            except Exception as e:
                return Response({'error': f'{e}'}, status=status.HTTP_404_NOT_FOUND)
        else:
            cards = CardDetail.objects.all()
            serializer = CardDetailSerializer(cards, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request,id = None):
        if id:
            return Response({'msg': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = CardDetailSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Card Created'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
from django.http import HttpResponse    

def sendMain1(request):
    subject = "Test Greetings"
    message = "Hope you are having a great day!"
    email_from = settings.EMAIL_HOST_USER
    receipient_list = ['harshsam612@gmail.com',]
    send_mail(subject, message, email_from, receipient_list)

    return  HttpResponse("Mail Sent")


def sendMain(request):
    subject = "Test Greetings"
    message = "Hope you are having a great day!"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['harshsam612@gmail.com']

    try:
        send_mail(subject, message, email_from, recipient_list)
        success_message = "Mail Sent"
    except Exception as e:
        success_message = f"Mail could not be sent. Error: {str(e)}"


    return HttpResponse(success_message)