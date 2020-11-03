from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product,Order,Item,Address


class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ['id', 'name', 'price', 'img','stock', 'description', 'date_added', 'category']


class SignUpSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	class Meta:
		model = User
		fields = ['username', 'password']

	def create(self, validated_data):
		new_user = User(**validated_data)
		new_user.set_password(validated_data['password'])
		new_user.save()
		return validated_data

class AddressSerializer(serializers.ModelSerializer):
	class Meta:
		model= Address
		fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = Item
		fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
	items= ItemSerializer(many=True)
	class Meta:
		model = Order
		fields = ['id', 'uuid', 'customer', 'address',  'items', 'date_time', 'total']
