from django.shortcuts import render
from rest_framework.generics import ListAPIView,CreateAPIView, RetrieveAPIView
from .serializers import  (
	ProductSerializer,OrderSerializer,SignUpSerializer,AddressSerializer,
	ProfileSerializer, ItemSerializer,StockSerializer
)
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
		return self.request.user.orders.filter(is_paid=True)


class CartView(APIView):
	serializer_class = OrderSerializer
	permission_classes = [IsAuthenticated]
	def get(self, request):
		order, _ = Order.objects.get_or_create(
			customer=self.request.user, is_paid=False
		)
		return Response(self.serializer_class(order).data, status=HTTP_200_OK)


class ProfileView(RetrieveAPIView):
	serializer_class = ProfileSerializer
	
	def get_object(self):
		return self.request.user.profile


class AddressCreateView(CreateAPIView):
	serializer_class = AddressSerializer
	permission_classes = [IsAuthenticated]
	# Need to use perform create to set user profile



class OrderItems(APIView):
	serializer_class = OrderSerializer
	permission_classes = [IsAuthenticated]

	def post(self, request):
		new_order, _ = Order.objects.get_or_create(customer=self.request.user, is_paid=False)
		item, added = Item.objects.get_or_create(product=Product.objects.get(id=request.data['product_id']),order=new_order)

		if added:
			item.quantity=request.data['quantity']
		else:
			item.quantity += request.data['quantity']
		item.save()

		new_total = (int(request.data['quantity'])*float(item.product.price))+float(new_order.total)
		new_order.total = new_total
		new_order.save()
		return Response(self.serializer_class(new_order).data, status=HTTP_200_OK)


class RemoveItems(APIView):
	serializer_class = OrderSerializer

	def post(self, request):
		order = Order.objects.get(customer=self.request.user, is_paid=False)
		product = Product.objects.get(id=request.data['product_id'])
		try:
			old_item = Item.objects.get(
				product_id=request.data['product_id'],
				order=order
			)
			order.total -= (old_item.quantity*product.price)
			order.save()

			old_item.delete()
			return Response(self.serializer_class(order).data, status=HTTP_200_OK)
		except:
			return Response({"msg": "Something went wrong"}, status=HTTP_400_BAD_REQUEST)



class Checkout(APIView):
	serializer_class = StockSerializer
	permission_classes = [IsAuthenticated]
	def post(self, request):
		order = Order.objects.get(customer=self.request.user, is_paid=False)
		items = order.items.all()

		if order.all_items_in_stock():
			for item in items:
				order.is_paid=True
				order.save()
				for x in items:
					x.product.stock-=x.quantity
					x.product.save()
					return Response({}, status=HTTP_200_OK)
		else:
			return Response({
				"msg": "Some items in your cart are out of stock"
			}, status=HTTP_400_BAD_REQUEST)
