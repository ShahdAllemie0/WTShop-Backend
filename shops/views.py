from django.shortcuts import render
from rest_framework.generics import ListAPIView,CreateAPIView
from .serializers import  ProductSerializer,OrderSerializer,SignUpSerializer,AddressSerializer
from .models import Product,Order,Item,Address
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import uuid


class SignUpAPIView(CreateAPIView):
	serializer_class = SignUpSerializer


class ProductListView(ListAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	permission_classes = [AllowAny]


class AddressCreateAPIView(CreateAPIView):
	serializer_class = AddressSerializer
	permission_classes = [AllowAny]
	# Permission needs to be set to IsAuthenticated
	# Need to use perform create to set user profile



class OrderItems(APIView):
	serializer_class = OrderSerializer

	def post(self, request):

		order, created = Order.objects.get_or_create(customer=self.request.user, is_paid=False)

		# Scenario 1, the item is already in the cart, increment quantity
		# Scenario 2, the item is not in the cart, assign
		# = Item.objects.get_or_create(product=, order=)

		return Response(self.serializer_class(order_obj).data, status=HTTP_200_OK)
