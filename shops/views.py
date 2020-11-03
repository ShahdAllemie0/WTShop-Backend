from django.shortcuts import render
from rest_framework.generics import ListAPIView,CreateAPIView
from .serializers import  ProductSerializer,OrderSerializer,SignUpSerializer,AddressSerializer
from .models import Product,Order,Item,Address
from rest_framework.views import APIView
import uuid


class SignUpAPIView(CreateAPIView):
	serializer_class = SignUpSerializer


class ProductListView(ListAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer

class AddressCreateAPIView(CreateAPIView):
	serializer_class = AddressSerializer


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
