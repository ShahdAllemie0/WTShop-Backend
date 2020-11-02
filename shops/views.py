from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView, ListAPIView
from .serializers import  ProductDetailsSerializer, ProductsListSerializer
from .models import Product



class ProductListView(ListAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductsListSerializer


class ProductDetails(RetrieveAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductDetailsSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'product_id'
