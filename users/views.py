from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from .models import user, CardDetail, otp
from rest_framework.views import APIView 
from .serializers import UserSerializer as userSerializer
from .serializers import CardDetailSerializer 
from django.conf import settings
from product.models import cart

from django.core.mail import send_mail
from django.conf import settings



class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user_obj = user.objects.get(username=username)
            serializer = userSerializer(user_obj)
            if user_obj.check_password(password):
                return Response({
                    "msg": "Login Successfull",
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

                    print(userObj)
                    print(userObj.id)
                    otpObj = otp.objects.create(user=userObj, otp=createOTP())
                    print(request.data['fullname'],otpObj.otp,request.data['email'])
                    mail_otp(userObj.fullname,otpObj.otp,userObj.email)

                    #userObj = user.objects.get(email=request.data['email']) 
                    #print(userObj)        
                    
                    return Response({
                        'msg': 'User Created',
                        'user': serializer.data,    
                        }, status=status.HTTP_201_CREATED)
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


from django.utils import timezone
from datetime import timedelta

class OTPVerifyView(APIView):
    
    def post(self,request):
        try:
            otpObj = otp.objects.get(otp=request.data['otp'])

            if otpObj.user == request.data['user'] or otpObj.created_at > timezone.now() - timedelta(minutes=5) or True:
                otpObj.delete()
                userobj = user.objects.get(id=request.data['user'])
                userobj.is_active = True
                userobj.save()

                receiver = [userobj.email]
                send_mail(
                    "Furniture app - Welcome to Furniture app",
                    'Your profile has been activated successfully.',
                    settings.EMAIL_HOST_USER,
                    receiver,
                    fail_silently=False
                )

                return Response({'msg': 'OTP verified'}, status=status.HTTP_200_OK)

            elif otpObj.created_at > timezone.now() - timedelta(minutes=5):
                
                otpObj.delete()
                return Response({'msg': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'msg': 'OTP not verified'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)


def createOTP():
    import random
    otp = random.randint(100000, 999999)
    return otp 

def mail_otp(name,otp,email):    

    try:
        user = name
        OTP = otp
        receiver = [email]
        
        message = f'''<div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
<div style="margin:50px auto;width:80%;padding:20px 0">
<div style="border-bottom:5px solid #eee">
  <a href="" style="font-size:30px;color: #f7c800;text-decoration:none;font-weight:600">Furniture App</a>
</div>
<p style="font-size:15px">Hello {user},</p>
<p>Thank you for choosing furniture app. Use this OTP to complete your Sign Up procedures and verify your account on Furniture app.</p>
<p>Remember, Never share this OTP with anyone.</p>
<h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{OTP}</h2>
<p style="font-size:15px;">Regards,<br />Team Furniture app</p>
<hr style="border:none;border-top:5px solid #eee" />
<div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">

 </div>
</div>
</div>'''
        send_mail(
            "Furniture app - email verification",
            '',
            settings.EMAIL_HOST_USER,
            receiver,
            fail_silently=False,
            html_message=message
        )
        return True
    except Exception as e:
        print(e)
        return False

class forgotPassword(APIView):
    
    def post(self,request):
        try:
            user_obj = user.objects.get(email=request.data['email'])
            otpObj = otp.objects.create(user=user_obj, otp=createOTP())
            print(user_obj.fullname,otpObj.otp,user_obj.email)
            send_mail(
                "Furniture app - Forgot password",
                f'Hello {user_obj.fullname},\nUse this OTP to reset your password.\n{otpObj.otp}',
                settings.EMAIL_HOST_USER,
                [user_obj.email],
                fail_silently=False
            )
            
            
            return Response({'msg': 'OTP sent'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)


class SendOTPView(APIView):
    def get(self,request):
        try:
            mail_otp("Harsh",123456,"harshmangroliya0@gmail.com")
            
            return Response({'msg': 'OTP sent'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)