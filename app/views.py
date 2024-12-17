from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
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
def login(request):
    return render(request,'app/login.html')
def tracking(request):
    return render(request,'app/tracking.html')
def elements(request):
    return render(request,'app/elements.html')
def contact(request):
    return render(request,'app/contact.html')