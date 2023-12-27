from .models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ProductSerializer, ProductImageSerializer

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



    
   