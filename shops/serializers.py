from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product



class ProductsListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ['id', 'name',  'img']



class ProductDetailsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ['id', 'name', 'price', 'img','stock', 'description', 'date_added', 'category']
    
