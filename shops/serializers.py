from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product,Order,Item,Address
from rest_framework_jwt.settings import api_settings



class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ['id', 'name', 'price', 'img','stock', 'description', 'date_added', 'category']


class SignUpSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	token = serializers.CharField(allow_blank=True, read_only=True)

	class Meta:
		model = User
		fields = ['username', 'password', 'token']

	def create(self, validated_data):
		username = validated_data['username']
		password = validated_data['password']
		new_user = User(username=username)
		new_user.set_password(password)
		new_user.save()

		jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
		jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

		payload = jwt_payload_handler(new_user)
		token = jwt_encode_handler(payload)

		validated_data["token"] = token
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
	customer = serializers.SlugRelatedField(
        many=False,  # it's by Default
        read_only=True,
        slug_field='username')
		#total = serializers.SerializerMethodField()
    
	class Meta:
		model = Order
		fields = ['uuid', 'customer', 'address',  'items', 'date_time', 'total']
