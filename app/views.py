from itertools import product
from multiprocessing import context
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import json


# Create your views here.
def register(request): 
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request,'app/register.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else: messages.info(request, 'Username or Password is not correct!!')
    return render(request,'app/login.html')

def logoutPage(request):
    logout(request)
    return redirect('home')

def home(request):
    products = Product.objects.all()
    context = {'products': products}    
    return render(request,'app/homepage.html', context)

def category(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request,'app/category.html',context)

def single_product(request):
    id = request.GET.get('id', '')

    product = Product.objects.get(id=id)

    context = { 'product': product }    

    return render(request,'app/single-product.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
    else:
        items = []
        cart = {'get_cart_total':0, 'get_cart_items':0}
        customer = None
    context = {'items':items, 'cart':cart, 'customer':customer}
    return render(request,'app/checkout.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
    else:
        items = []
        cart = {'get_cart_total':0, 'get_cart_items':0}
    context = {'items':items, 'cart':cart}
    return render(request,'app/cart.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    cart, created = Cart.objects.get_or_create(customer=customer)
    cartItem, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if action == 'add':
        cartItem.quantity = (cartItem.quantity + 1)
    elif action == 'remove':
        cartItem.quantity = (cartItem.quantity - 1)
    cartItem.save()
    if cartItem.quantity <= 0:
        cartItem.delete()
    return JsonResponse('Item was added', safe=False)

def confirmation(request):
    return render(request,'app/confirmation.html')

def blog(request):
    return render(request,'app/blog.html')

def single_blog(request):
    return render(request,'app/single-blog.html')

def tracking(request):
    return render(request,'app/tracking.html')

def contact(request):
    return render(request,'app/contact.html')