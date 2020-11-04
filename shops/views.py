from django.shortcuts import render
from rest_framework.generics import ListAPIView,CreateAPIView
from .serializers import  ProductSerializer,OrderSerializer,SignUpSerializer,AddressSerializer,UserLoginSerializer
from .models import Product,Order,Item,Address
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import uuid

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

		order_obj ={}
		item_obj={}
		try:
			order_obj = Order.objects.get(customer=self.request.user, isPaid=False)
		except:
  			print("An exception occurred")
		new_data = request.data
		new_product = Product.objects.get(id=new_data['product_id'])
		# total_new=order_obj.total
		if not order_obj:

			new_order ={
				'uuid': str(uuid.uuid4())[0:8],
				'customer':self.request.user,
				'isPaid':False,
				'total':(int(new_data['quantity'])*float(new_product.price))
			}
			order_obj= Order.objects.create(**new_order)
			order_obj.save()



		try:
			item_obj = Item.objects.get(product=new_product)
		except:
  			print("An exception occurred")
		if item_obj:
			item_obj.quantity += int(new_data['quantity'])
			item_obj.save()
			order_obj.total=(int(new_data['quantity'])*float(new_product.price))+float(order_obj.total)
			order_obj.save()
		else:


			new_item = {
				'product': new_product,
				'quantity': new_data['quantity'],
				'order':order_obj,
			}
			item = Item.objects.create(**new_item)
			item.save()
		return Response(self.serializer_class(order_obj).data, status=HTTP_200_OK)
