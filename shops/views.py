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

		new_order, created = Order.objects.get_or_create(customer=self.request.user, is_paid=False)
		new_product=Product.objects.get(id=request.data['product_id'])
		item, added = Item.objects.get_or_create(product=new_product,order=new_order)
		if item.product.stock>=int(request.data['quantity']):
			if added:
				item.quantity=request.data['quantity']
				item.save()
			else:
				item.quantity=int(request.data['quantity'])+int(item.quantity)
				item.save()

			new_product.stock=int(item.product.stock)-int(request.data['quantity'])
			# item.save()
			new_product.save()
			new_order.total=(int(request.data['quantity'])*float(item.product.price))+float(new_order.total)
			new_order.save()
			return Response(self.serializer_class(new_order).data, status=HTTP_200_OK)
		else:
			return Response(self.serializer_class().data, status=HTTP_400_BAD_REQUEST)
