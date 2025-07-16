
from django.contrib import admin
from django.urls import path, re_path
from . import views
from .views import *

urlpatterns = [
    re_path('products', views.products, name='products'),
    re_path('artists', views.artists, name='artists'),
    re_path('genres', views.genres, name='genres'),
    re_path('category', views.category, name='category'),
    path('product_detail/<slug:slug>', views.product_detail, name="product_detail"),
    path('add_item/', views.add_item, name="add_item"),
    path('product_in_cart', views.product_in_cart, name="product_in_cart"), 
    path('get_cart_stat', views.get_cart_stat, name="get_cart_stat"), 
    path('get_cart', views.get_cart, name="get_cart"), 
    path('upadate_quantity/', views.upadate_quantity, name="upadate_quantity"), 
    path('delete_cartitem/', views.delete_cartitem, name="delete_cartitem"), 
    path('user_info', views.user_info, name="user_info"), 
    path('register/', RegisterView.as_view(), name='register'),
    
    # path('create_order/', create_order, name='create_order'),
    # path('order_history/', order_history, name='order_history'),
]
