from django.shortcuts import render
from rest_framework.generics import ListAPIView,CreateAPIView, RetrieveAPIView
from .serializers import  (ProductSerializer,OrderSerializer,SignUpSerializer,AddressSerializer,ProfileSerializer,
  ItemSerializer)
from .models import Product,Order,Item,Address,Profile
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import uuid



class SignUpAPIView(CreateAPIView):
	serializer_class = SignUpSerializer


class ProductListView(ListAPIView):
	queryset = Product.objects.filter(stock__gte=1)
	serializer_class = ProductSerializer
	permission_classes = [AllowAny]

class OrderHistory(ListAPIView):
	serializer_class = OrderSerializer
	permission_classes = [IsAuthenticated]
	def get_queryset(self):
		return Order.objects.filter(customer=self.request.user, is_paid=True)


class CartView(RetrieveAPIView):
	serializer_class = OrderSerializer
	permission_classes = [IsAuthenticated]
	def get_object(self):
		return Order.objects.get(customer=self.request.user, is_paid=False)


class ProfileView(ListAPIView):
	serializer_class = ProfileSerializer
	def get_queryset(self):
		return Profile.objects.filter(user=self.request.user)


class AddressCreateView(CreateAPIView):
	serializer_class = AddressSerializer
	permission_classes = [AllowAny]
	# Permission needs to be set to IsAuthenticated
	# Need to use perform create to set user profile



class OrderItems(APIView):
	serializer_class = ItemSerializer
	permission_classes = [AllowAny]

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
			new_product.save()
			new_order.total=(int(request.data['quantity'])*float(item.product.price))+float(new_order.total)
			new_order.save()
			return Response(self.serializer_class(item).data, status=HTTP_200_OK)
		else:
			return Response(self.serializer_class().data, status=HTTP_400_BAD_REQUEST)

class RemoveItems(APIView):
	serializer_class = ItemSerializer

	def post(self, request):
		order = Order.objects.get(customer=self.request.user, is_paid=False)
		product = Product.objects.get(id=request.data['product_id'])
		try:
			old_item = Item.objects.get(
				product_id=request.data['product_id'],
				order=order
			)
			
			product.stock += old_item.quantity
			product.save()
			
			order.total -= (old_item.quantity*product.price)
			order.save()

			old_item.delete()
			return Response({}, status=HTTP_200_OK)
		except:
			return Response({}, status=HTTP_400_BAD_REQUEST)
# c/gt4
