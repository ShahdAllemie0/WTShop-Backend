from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product,Order,Item,Address
from rest_framework_jwt.settings import api_settings



class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ['id', 'name', 'price', 'img','stock', 'description', 'date_added', 'category']

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(allow_blank=True, read_only=True)

    def validate(self, data):
        my_username = data.get('username')
        my_password = data.get('password')

        try:
            user_obj = User.objects.get(username=my_username)
        except:
            raise serializers.ValidationError("This username does not exist")

        if not user_obj.check_password(my_password):
            raise serializers.ValidationError(
                "Incorrect username/password combination! Noob..")

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)

        data["token"] = token
        return data

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
