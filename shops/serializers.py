from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product,Order,Item,Address,Profile
from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken


class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ['id', 'name', 'price', 'img','stock', 'description', 'date_added', 'category']


class SignUpSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	token = serializers.CharField(allow_blank=True, read_only=True)

	class Meta:
		model = User
		fields = ['username', 'email','first_name', 'last_name', 'password','token']

	def create(self, validated_data):

		new_user = User(**validated_data)
		new_user.set_password(validated_data['password'])
		new_user.save()
		token = RefreshToken.for_user(new_user)
		validated_data["token"] = str(token.access_token)
		return validated_data




class AddressSerializer(serializers.ModelSerializer):
	class Meta:
		model= Address
		fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model= Profile
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
		fields = [ 'customer', 'address',  'items', 'date_time', 'total']
