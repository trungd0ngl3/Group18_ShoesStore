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
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
        cartItems = cart.get_cart_items

    else:
        items = []
        cart = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = cart['get_cart_total']
        customer = None

    products = Product.objects.filter().order_by('-id')[:8]
    context = {'products': products, 'cartItems': cartItems}    
    return render(request,'app/homepage.html', context)

def category(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
        cartItems = cart.get_cart_items

    else:
        items = []
        cart = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = cart['get_cart_total']
        customer = None

    products = Product.objects.all()
    sort_option = request.GET.get('sort_option', '')

    if sort_option != '':
        products = Product.objects.filter(description=sort_option)
    if sort_option == 'All':
        products = Product.objects.all()
    
    context = {'products': products, 'cartItems': cartItems}
    return render(request,'app/category.html',context)

def single_product(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
        cartItems = cart.get_cart_items

    else:
        items = []
        cart = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = cart['get_cart_total']
        customer = None

    id = request.GET.get('id', '')

    product = Product.objects.get(id=id)

    context = { 'product': product , 'cartItems': cartItems}    

    return render(request,'app/single-product.html', context)

def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()        
        cartItems = cart.get_cart_items
    else:
        return redirect('login')
    
    context = {'items':items, 'cart':cart, 'customer':customer, 'cartItems':cartItems}
    return render(request,'app/checkout.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
        cartItems = cart.get_cart_items
    else:
        items = []
        cart = {'get_cart_total':0, 'get_cart_items':0}
        cartItems=0
    context = {'items':items, 'cart':cart, 'cartItems':cartItems}
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

def search(request):
    if request.method == 'POST':
        query = request.POST['query']
        products = Product.objects.filter(name__icontains=query)
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
        cartItems = cart.get_cart_items
    else:
        items = []
        cart = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = cart['get_cart_total']
        customer = None
    context = {'products': products, 'cartItems': cartItems, 'query': query}
    return render(request,'app/search.html',context)

def confirmation(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
        cartItems = cart.get_cart_items
        billing  = BillingAddress.objects.get(customer=customer)
        shipping = ShippingAddress.objects.get(customer=customer)
    else:
        items = []
        cart = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = cart['get_cart_total']
        customer = None

    context = {'items':items, 'cart':cart, 'customer':customer, 'cartItems':cartItems, 'billing':billing, 'shipping':shipping}
    return render(request,'app/confirmation.html',context)

def tracking(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()        
        cartItems = cart.get_cart_items
    else:
        items = []
        cart = {'get_cart_total':0, 'get_cart_items':0}
        customer = None
        cartItems=0
    context = {'items':items, 'cart':cart, 'customer':customer, 'cartItems':cartItems}
    return render(request,'app/tracking.html',context)

def contact(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()        
        cartItems = cart.get_cart_items
    else:
        items = []
        cart = {'get_cart_total':0, 'get_cart_items':0}
        customer = None
        cartItems=0
    context = {'items':items, 'cart':cart, 'customer':customer, 'cartItems':cartItems}
    return render(request,'app/contact.html',context)