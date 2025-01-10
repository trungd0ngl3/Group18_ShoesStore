from dataclasses import field
from django.utils.timezone import now
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
# Create your models here.
# Change forms register django
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}),
                    'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'First name'}),
                    'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last name'}),
                    'email':forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}),
                   
        }
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm password'})

# --------

class Promotion(models.Model):
    code = models.CharField(max_length=200, null=True)
    discount = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):  
        return self.code

    def is_valid(self):
        return self.start_date <= now().date() <= self.end_date



class ShippingAddress(models.Model):
    address =  models.CharField(max_length=200,null=True)
    city =  models.CharField(max_length=200,null=True)
    state =  models.CharField(max_length=200,null=True)
    zipcode =  models.CharField(max_length=200,null=True)
    country =  models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.address
    
class BillingAddress(models.Model):
    address =  models.CharField(max_length=200,null=True)
    city =  models.CharField(max_length=200,null=True)
    state =  models.CharField(max_length=200,null=True)
    zipcode =  models.CharField(max_length=200,null=True)
    country =  models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.address

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    manufacturer = models.CharField(max_length=200, null=True)
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL,blank=True,null=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_discount_price(self):
        if self.promotion:
            return self.price - self.price * self.promotion.discount/100
        return self.price

    def get_discount(self):
        if self.promotion:
            return self.price * self.promotion.discount
        return 0

class Cart(models.Model):
    cart_id = models.CharField(max_length=200)
    total_price = models.FloatField(default=0)
    def __str__(self):
        return self.cart_id

    def get_cart_total(self):
        cart_items = self.cartitem_set.all() 
        return sum([item.get_subtotal() for item in cart_items])   
    def get_cart_items(self):
        cart_items = self.cartitem_set.all()
        return sum([item.quantity for item in cart_items])


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,blank=True,null=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    def __str__(self):
        return self.product.name
    def get_subtotal(self):
        return self.product.get_discount_price() * self.quantity

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=False)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL,null=True,blank=True)
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.SET_NULL,null=True,blank=True)
    cart = models.ForeignKey(Cart,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class SalesOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,blank=True,null=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL,blank=True,null=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL,blank=True,null=True)
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return self.customer.first_name + ' ' + self.customer.last_name