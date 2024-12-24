from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('category',views.category,name='category'),
    path('product-details',views.single_product,name='product-details'),
    path('checkout',views.checkout,name='checkout'),
    path('cart',views.cart,name='cart'),
    path('confirmation',views.confirmation,name='confirmation'),
    path('blog',views.blog,name='blog'),
    path('blog-details',views.single_blog,name='blog-details'),
    path('login',views.loginPage,name='login'),
    path('logout',views.logoutPage,name='logout'),
    path('register',views.register,name='register'),
    path('tracking',views.tracking,name='tracking'),
    path('contact',views.contact,name='contact'),
    
]