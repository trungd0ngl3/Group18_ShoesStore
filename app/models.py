from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django.forms import CharField
# Create your models here.

class ShippingAddress(models.Model):
    address =  models.CharField(max_length=200,null=True)
    city =  models.CharField(max_length=200,null=True)
    state =  models.CharField(max_length=200,null=True)
    zipcode =  models.CharField(max_length=200,null=True)
    country =  models.CharField(max_length=200,null=True)
    
class BillingAddress(models.Model):
    address =  models.CharField(max_length=200,null=True)
    city =  models.CharField(max_length=200,null=True)
    state =  models.CharField(max_length=200,null=True)
    zipcode =  models.CharField(max_length=200,null=True)
    country =  models.CharField(max_length=200,null=True)

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    desciption = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    manufacturer = models.CharField(max_length=200, null=True)
    
class Cart(models.Model):
    cart_id = models.CharField(max_length=200)
    total_price = models.FloatField(default=0)
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,blank=True,null=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=False)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL,null=True,blank=True)
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.SET_NULL,null=True,blank=True)
    cart = models.ForeignKey(Cart,on_delete=models.SET_NULL,null=True,blank=True)

class SalesOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,blank=True,null=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL,blank=True,null=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL,blank=True,null=True)
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.SET_NULL,blank=True,null=True)
