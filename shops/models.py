from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import uuid



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


class Profile(models.Model):
	GENDER = (
		("F", "Female"),
		("M", "Male")
	)
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	phone = models.PositiveIntegerField(null=True)
	gender = models.CharField(choices=GENDER, max_length=2, null=True)
	image = models.ImageField(null=True)

	def __str__(self):
		return self.user.username

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user= instance)


class Address(models.Model):
	country = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	street = models.CharField(max_length=200)
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='addresses')
	
	def __str__(self):
		return f"{self.profile.user.username}: {self.country}-- {self.city}"



class Order(models.Model):
	#uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	uuid = models.CharField(max_length=10)
	address =models.ForeignKey(Address, on_delete=models.CASCADE,blank=True,null=True, related_name='orders')
	customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
	date_time = models.DateTimeField(auto_now_add=True)
	is_paid=models.BooleanField(default=False)
	total = models.DecimalField(max_digits=6, decimal_places=2,blank=True,null=True)

	def __str__ (self):
		return ("Order uuid: " + self.uuid)


class Item(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
	quantity = models.PositiveIntegerField()
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')

	def __str__(self):
		return f"{self.product.name}: ({self.quantity})"
