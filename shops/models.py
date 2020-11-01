from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
# Create your models here.

		# *******Product******
class Product(models.Model):

	CATEGORY = (
		("Drink", "Drinks"),
		("Food", "Food")
	)
	name=models.CharField(max_length=120)
	price=models.DecimalField(max_digits=6, decimal_places=3)
	img=models.ImageField()
	stock=models.PositiveIntegerField()
	description=models.TextField()
	date_added=models.DateField(auto_now=True)
	category = models.CharField(choices=CATEGORY, max_length=8, null=True, blank=True)

	def __str__ (self):
		return self.name


		# *******Customer******
class Customer(models.Model):
	GENDER = (
		("F", "Female"),
		("M", "Male")
	)
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
	phone = models.PositiveIntegerField(null=True)
	gender = models.CharField(choices=GENDER, max_length=1, null=True)
	age = models.PositiveIntegerField(null=True)
	image = models.ImageField(null=True)
	address=models.TextField()


	def __str__(self):
		return self.user.username


		# *******Order******
class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
	date_time = models.DateTimeField(auto_now_add=True)
	total = models.DecimalField(max_digits=10, decimal_places=4)



		# *******Order******
class Cart(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
	quantity = models.PositiveIntegerField()
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='carts')
