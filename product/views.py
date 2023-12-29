from .models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ProductSerializer, ProductImageSerializer, cartSetializer

class ProductView(APIView):

    allowed_methods = ['GET', 'POST', 'PATCH']

    def get(self, request,id = None):
        if id:
            try:
                product_obj = Product.objects.get(id=id)
                serializer = ProductSerializer(product_obj)

                productImage_obj = productImage.objects.filter(product=id)
                imageserializer = ProductImageSerializer(productImage_obj, many=True)

                jsondata = serializer.data
                jsondata['images'] = []
                for i in imageserializer.data:
                    jsondata['images'].append(i['image'])

                return Response(jsondata, status=status.HTTP_200_OK)
            
            except Product.DoesNotExist:
                return Response({'msg': 'Product does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            jsondata = serializer.data
            for i in jsondata:
                productImage_obj = productImage.objects.filter(product=i['id']).first()
                imageserializer = ProductImageSerializer(productImage_obj)
                i['image'] = imageserializer.data['image']
            return Response(jsondata, status=status.HTTP_200_OK)

    def post(self, request,id = None):
        if id:
            return Response({'msg': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Product Created'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    def patch(self, request,id = None):
        if id:
            try:
                product_obj = Product.objects.get(id=id)
                serializer = ProductSerializer(product_obj, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'msg': 'Product Updated'}, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Product.DoesNotExist:
                return Response({'msg': 'Product does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'msg': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)

class cartView(APIView):
    
    def get(self,request,id=None):
        if id:
            try:
                products_in_cart = cart.objects.filter(user=id)
                serializer = cartSetializer(products_in_cart, many=True)
                if serializer.is_valid():
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'msg': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)
            
    def post(self,request,id=None):
        print(request.data)
        obj = cart.objects.filter(product=request.data['product'],user=request.data['user']).first()
        if obj:
            # print(obj.quantity)
            # print("##############")
            obj.updateQty(request.data['quantity'])

            return Response({'msg': 'Product quantity updated'}, status=status.HTTP_202_ACCEPTED)
        serializer = cartSetializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Product Added to Cart'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,id=None):
        
        obj = cart.objects.get(user = request.data['user'],product= request.data['product'])
        if obj:
            obj.updateQty(request.data['quantity'])
            return Response({'msg': 'Product quantity updated'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'msg': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id=None):
        obj = cart.objects.get(product=request.data['product'],user=request.data['user'])
        if obj:
            obj.delete()
            return Response({'msg': 'cart deleted'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'msg': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)            
            
    
   