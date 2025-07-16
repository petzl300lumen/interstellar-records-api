from django.contrib import admin
from .models import *

admin.site.register([Products, Genres, Category, Artists, Cart, CartItem, Statuses, Orders, OrderItem])

