from django.shortcuts import render
from rest_framework.generics import ListAPIView,CreateAPIView
from .serializers import  ProductSerializer,OrderSerializer,SignUpSerializer,AddressSerializer,UserLoginSerializer
from .models import Product,Order,Item,Address
from rest_framework.views import APIView
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
	# serializer_class = OrderSerializer

	def post(self, request):

		new_user=request.user
		order = Order.objects.filter(customer = new_user )
		if order:
			cart=Order.objects.get(customer=new_user)
		else:
			cart=Order.objects.create(customer=new_user)
		new_data=request.data
		serializer=self.serializer_class(data=new_data)
		if serializer.is_valid():
			valid_data = serializer.data
			new_data = {
				'product': Product.objects.get(id=valid_data['product_id']),
				'quantity': valid_data['quantity'],
				'order':cart
			}
			new_item = Item.objects.create(**new_data)
		return Response(self.serializer_class(cart).data, status=HTTP_200_OK)

		# total = 0

		 # total
		 #Address

		# order
		# order  = Order.objects.create(order_ref= new_uuid, customer = request.user, address= , total=)

		 # item
		# Item.objects.create(product_id=,quantity=,order=order)


# class CreateOrder(CreateAPIView):
