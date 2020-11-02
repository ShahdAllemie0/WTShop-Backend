from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver


class Category(models.Model):
	name=models.CharField(max_length=120)

	def __str__ (self):
		return self.name


class Product(models.Model):
	name=models.CharField(max_length=120)
	price=models.DecimalField(max_digits=6, decimal_places=3)
	img=models.ImageField()
	stock=models.PositiveIntegerField()
	description=models.TextField()
	date_added=models.DateField(auto_now_add=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

	def __str__ (self):
		return self.name


class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone = models.PositiveIntegerField(null=True)
	image = models.ImageField(null=True)
	address=models.TextField()

	def __str__(self):
		return self.user.username


class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
	quantity = models.PositiveIntegerField()
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')

	def __str__(self):
		return f"{self.product.name}: ({self.quantity})"


class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
	date_time = models.DateTimeField(auto_now_add=True)
	# status = 
	total = models.DecimalField(max_digits=10, decimal_places=4)

	def __str__(self):
		return f"{self.customer.user.username}'s order"

