from django.shortcuts import render
from rest_framework.generics import ListAPIView,CreateAPIView
from .serializers import  ProductSerializer,OrderSerializer,SignUpSerializer,AddressSerializer,UserLoginSerializer
from .models import Product,Order,Item,Address
from rest_framework.views import APIView
import uuid
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        my_data = request.data
        serializer = UserLoginSerializer(data=my_data)
        if serializer.is_valid(raise_exception=True):
            valid_data = serializer.data
            return Response(valid_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class SignUpAPIView(CreateAPIView):
	serializer_class = SignUpSerializer


class ProductListView(ListAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	permission_classes = [AllowAny]


class AddressCreateAPIView(CreateAPIView):
	serializer_class = AddressSerializer
	permission_classes = [AllowAny]



class OrderItems(APIView):
	serializer_class = OrderSerializer

	def post(self, request):
		new_uuid = str(uuid.uuid4())[0:8]
		total = 0

    	 # total
		 #Address

		# order
		# order  = Order.objects.create(order_ref= new_uuid, customer = request.user, address= , total=)

		 # item
		# Item.objects.create(product_id=,quantity=,order=order)
