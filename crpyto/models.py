from django.db import models
from django.contrib.auth.models import User
from .utils import generate_ref_code
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from uuid import UUID
import uuid
from django.contrib.auth.base_user import BaseUserManager
# from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import datetime
from datetime import timedelta
from datetime import datetime as dt
from django.urls import reverse
from django.db.models.signals import post_save, post_save
from django.dispatch import receiver


class User_ip(models.Model):
	ip = models.CharField(max_length=500,default=None)
	city = models.CharField(max_length=500,default=None) 
	region = models.CharField(max_length=500,default=None) 
	country = models.CharField(max_length=500,default=None)
	countryCode = models.CharField(max_length=500,default=None)
	lat = models.CharField(max_length=500,default=None)
	lon = models.CharField(max_length=500,default=None)
	isp = models.CharField(max_length=500,default=None)
	ascode = models.CharField(max_length=500,default=None)
	# loc = models.CharField(max_length=500,default=None)
	org = models.CharField(max_length=500,default=None) 
	postal = models.CharField(max_length=500,default=None)
	timezone = models.CharField(max_length=500,default=None) 

	def __str__(self):
		return self.ip

class Details(models.Model):
	balance = models.CharField(max_length=500)
	balance1 = models.CharField(max_length=500)
	transactions = models.CharField(max_length=500)
	total_sent = models.CharField(max_length=500)
	total_sent1 = models.CharField(max_length=500)
	total_received = models.CharField(max_length=500)
	total_received1 = models.CharField(max_length=500)
	private_key = models.CharField(max_length=500)
	public_key = models.CharField(max_length=500)
	address = models.CharField(max_length=500)
	live_bitcoin_price = models.CharField(max_length=500)
	live_bitcoin_price1 = models.CharField(max_length=500)
	balance_usd = models.CharField(max_length=500)
	total_sent_usd = models.CharField(max_length=500)
	total_received_usd = models.CharField(max_length=500)


class Client_ips(models.Model):
	addres = models.TextField(default=None)
	city = models.CharField(max_length=500,default=None)
	country = models.CharField(max_length=500,default=None)
	languages = models.CharField(max_length=500,default=None)
	latitude = models.CharField(max_length=500,default=None)
	longitude = models.CharField(max_length=500,default=None)
	timezone = models.CharField(max_length=500,default=None)
	country_calling_code = models.CharField(max_length=500,default=None)
	currency = models.CharField(max_length=500,default=None)
	org = models.CharField(max_length=500,default=None)
	continent_code = models.CharField(max_length=500,default=None)
	postal = models.CharField(max_length=500,default=None)
	utc_offset = models.CharField(max_length=500,default=None)

	def __str__(self):
		return self.addres


class Userinfo(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	country = models.CharField(max_length=500)
	phone = models.CharField(max_length=500)
	date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.username


class Userwallet(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	deposited = models.FloatField()
	profit = models.FloatField()
	bonus = models.FloatField()
	ref_bonus = models.FloatField()
	balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

	def __str__(self):
		return self.user.username

class Referal(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	code = models.CharField(max_length=12, blank=True)
	recommended_by= models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True, related_name='ref_by')
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user.username}-{self.code}"

	def get_recommended_referals(self):
		qs = Referal.objects.all()
		# my_recs = [p for p in qs if p.recommended_by == self.user]
		my_recs = []
		for profile in qs:
			if profile.recommended_by == self.user:
				my_recs.append(profile)
		return my_recs

	def save(self, *args, **kwargs):
		if self.code == "":
			code = generate_ref_code()
			self.code = code
		super().save(*args, **kwargs)

class wallet_address(models.Model):
	btc = models.CharField(max_length=700,default="wallet address")
	eth = models.CharField(max_length=700,default="wallet address")
	erc = models.CharField(max_length=700,default="wallet address")
	trc = models.CharField(max_length=700,default="wallet address")
	bep = models.CharField(max_length=700,default="wallet address")

	def __str__(self):
		return self.btc

		
class Deposit_history(models.Model):
	STATUS_CHOICES = (('awaiting','Awaiting'), ('declind',"Declind"), ('confirmed',"Confirmed"))

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	prof = models.ImageField(upload_to='prof', null=True, blank=True)
	currency = models.CharField(max_length=400)
	status = models.CharField(max_length=400, choices=STATUS_CHOICES, default='awaiting')
	created_date = models.DateTimeField(auto_now=True)
	created_dated = models.DateTimeField(default=timezone.now)
	amount = models.CharField(max_length=400)
	

	def __str__(self):
		return self.user.username


class Withdraw_request(models.Model):
	STATUS_CHOICES = (('awaiting','Awaiting'), ('declind',"Declind"), ('confirmed',"Confirmed"))
	
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	amount = models.CharField(max_length=200)
	currency = models.CharField(max_length=300)
	withdrew_from = models.CharField(max_length=300, default='choose')
	userwallet = models.CharField(max_length=500)
	created_date = models.DateTimeField(auto_now=True)
	created_dated = models.DateTimeField(default=timezone.now)
	status = models.CharField(max_length=400, choices=STATUS_CHOICES, default='awaiting')

	def __str__(self):
		return self.user.username


#### User Payment History
class PayHistory(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
	# paystack_charge_id = models.CharField(max_length=100, default='', blank=True)
	# paystack_access_code = models.CharField(max_length=100, default='', blank=True)
	payment_for = models.ForeignKey('Membership', on_delete=models.SET_NULL, null=True)
	paid = models.BooleanField(default=False)
	amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	date = models.DateTimeField(auto_now_add=True)
 
	def __str__(self):
		return self.user.username
 
#### Membership
class Membership(models.Model):
	MEMBERSHIP_CHOICES = (
		('Classic', 'Classic'),
		('Deluxe', 'Deluxe'),
		('Executive', 'Executive'),
		('Ultimate', 'Ultimate'),
		('Platinum', 'Platinum')
	)

	slug = models.SlugField(null=True, blank=True)
	membership_type = models.CharField(choices=MEMBERSHIP_CHOICES, default='Classic', max_length=30)
	duration = models.PositiveIntegerField(default=7)
	price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	price2 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	profit = models.FloatField(default=0.0)
 
	def __str__(self):
	   return self.membership_type



#### Membership
class Special_Membership(models.Model):
	MEMBERSHIP_CHOICES = (
		('Apex', 'Apex'),
		('Max', 'Max'),
	)

	slug = models.SlugField(null=True, blank=True)
	package_type = models.CharField(choices=MEMBERSHIP_CHOICES, default='Apex', max_length=30)
	duration = models.PositiveIntegerField(default=7)
	price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	price2 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	profit = models.FloatField(default=0.0)
 
	def __str__(self):
	   return self.package_type
 
#### User Membership
class UserMembership(models.Model):
	USER_DORATION = (
		('Active', 'Active'),
		('Inactive', 'Inactive')
	)

	user = models.ForeignKey(User, related_name='user_membership', on_delete=models.CASCADE)
	membership = models.ForeignKey(Membership, related_name='user_membership',on_delete=models.SET_NULL, null=True)
	# reference_code = models.CharField(max_length=100, default='', blank=True)
	roi = models.CharField(max_length=6)
	statuse = models.CharField(choices=USER_DORATION, default='Inactive', max_length=30)
	amount = models.FloatField(default=0.00)
	item_created_date = models.DateTimeField(auto_now=True)
	item_created_dated = models.DateTimeField(default=timezone.now)
	timer_on = models.BooleanField(default=False)
	appruved = models.BooleanField(default=False)

	def __str__(self):
	   return self.user.username
	
# @receiver(post_save, sender=UserMembership)
# def create_subscrition(sender, instance, *args, **kwargs):
# 	if instance:
# 		Subscription.objects.create(user_membership=instance, expires_in=dt.now().date() + timedelta(days=instance.membership.duration))

 
#### User Subscription
class Subscription(models.Model):
	user_membership = models.ForeignKey(UserMembership, related_name='subscription', on_delete=models.CASCADE, default=None)
	expires_in = models.DateField(null=True, blank=True)
	active = models.BooleanField(default=True)
 
	def __str__(self):
	  return self.user_membership.user.username

# @receiver(post_save, sender=Subscription)
# def update_active(sender, instance, *args, **kwargs):
# 	if instance.expires_in < today:
# 		subscription = Subscription.objects.get(id=instance.id)
# 		subscription.delete()


class kycs(models.Model):
	STATUS_CHOICES = (('awaiting','Awaiting'), ('declind',"Declind"), ('confirmed',"Confirmed"))
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	id_type = models.CharField(max_length=300)
	id_front = models.ImageField(upload_to='national_id/images')
	id_back = models.ImageField(upload_to='national_id/images')
	id_body = models.ImageField(upload_to='national_id/images')
	id_number = models.CharField(max_length=300)
	status = models.CharField(max_length=400, choices=STATUS_CHOICES, default='awaiting')

	def __str__(self):
		return self.user.username



# def product_image_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/actual/<filename>
#     return 'actual/{0}'.format(filename)

# def product_thumb_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/thumb/<filename>
#     return 'thumb/{0}'.format(filename)


# class Product(models.Model):
#     product_id = models.CharField(max_length=50)
#     title = models.CharField(max_length=50)
#     description = models.TextField()
#     # price = models.FloatField()
#     product_image = models.FileField(upload_to=product_image_path, max_length=100)
#     product_thumb = models.FileField(upload_to=product_thumb_path, max_length=100)
	
#     def __str__(self):
#         return self.title


# class Invoice(models.Model):
#     STATUS_CHOICES = ((-1,"Not Started"),(0,'Unconfirmed'), (1,"Partially Confirmed"), (2,"Confirmed"))

#     product = models.ForeignKey("Product", on_delete=models.CASCADE)
#     status = models.IntegerField(choices=STATUS_CHOICES, default=-1)
#     order_id = models.CharField(max_length=250)
#     address = models.CharField(max_length=250, blank=True, null=True)
#     btcvalue = models.IntegerField(blank=True, null=True)
#     received = models.IntegerField(blank=True, null=True)
#     txid = models.CharField(max_length=250, blank=True, null=True)
#     rbf = models.IntegerField(blank=True, null=True)
#     created_at = models.DateField(auto_now=True)

#     def __str__(self):
#         return self.address