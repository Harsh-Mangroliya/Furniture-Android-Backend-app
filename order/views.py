from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from users.models import user
 
class order(APIView):
    def get(self,request,id=None):
        if id:
            orderobj = Order.objects.get(id=id)
            orderdetailobj = OrderDetail.objects.filter(order=orderobj)
            serializer = orderDetailSerializer(orderdetailobj,many=True)
            return Response({
                "success":True,
                "order":orderobj.id,
                "products":serializer.data
                },status=status.HTTP_200_OK)
        else:
            return Response({
                "success":False,
                "message":"Order id is required"
                },status=status.HTTP_400_BAD_REQUEST)

    def post(self,request,id=None):
        if id:
            return Response({
                "success":False,
                "message":"Invalid request"
                },status=status.HTTP_400_BAD_REQUEST)
        
        userid = user.objects.filter(id=request.data['user']).first()
        products = request.data['products']

        orderobj = Order.object.create(customer=userid)
        
        for i in products:
            OrderDetail.objects.create(
                order=orderobj,
                product=i['product'],
                quantity=i['quantity'],
                price = i['price']
                )

        return Response({
            "success":True,
            "order":orderobj.id
            },status=status.HTTP_201_CREATED)

class AllOrder(APIView):
    def get(self,request,id=None):
        if id:
            orders = Order.objects.filter(customer=id)
            jsondata = {}
            for i in orders:
                orderdetail = OrderDetail.objects.filter(order=i)
                serializer = orderDetailSerializer(orderdetail,many=True)
                jsondata[i.id] = serializer.data
            
            return Response({
                "success":True,
                "orders":jsondata
                },status=status.HTTP_200_OK)    
        else:
            return Response({
                "success":False,
                "message":"User id is required"
                },status=status.HTTP_400_BAD_REQUEST)
        


