from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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
    return render(request,'app/index.html')

def category(request):
    return render(request,'app/category.html')

def single_product(request):
    return render(request,'app/single-product.html')

def checkout(request):
    return render(request,'app/checkout.html')

def cart(request):
    return render(request,'app/cart.html')

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