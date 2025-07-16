from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model


class ProductsSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    genre = serializers.StringRelatedField()
    class Meta:
        model = Products
        fields = ["id", "title", "slug", "image", "descr", "price", "date", "category", "genre"] 

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artists
        fields = "__all__"
        
class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = "__all__"
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        
class DetailedProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    genre = serializers.StringRelatedField()
    class Meta:
        model = Products
        fields = ["id", "title", "slug", "image", "descr", "price", "date", "category", "genre"] 
        
        
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(read_only=True)
    total = serializers.SerializerMethodField()
    # cart = CartSerializer(read_only=True) 
    class Meta:
        model = CartItem
        # новые изменения здесь
        fields = ["id", "quantity", "product", "total"]
        # здесь
    def get_total(self, cartitem):
        price = cartitem.product.price * cartitem.quantity
        return price
        
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(read_only=True, many=True)
    sum_total = serializers.SerializerMethodField()
    num_of_items = serializers.SerializerMethodField()
    class Meta: 
        model = Cart 
        fields = ["id", "cart_code", "items", "sum_total", "num_of_items", "created_at", "modified_at"]
        # новые изменени здесь
    def get_sum_total(self, cart):
        items = cart.items.all()
        total = sum([item.product.price * item.quantity for item in items])
        return total
    def get_num_of_items(self,cart):
        items = cart.items.all() 
        total = sum([item.quantity for item in items])
        return total
    
class SimpleCartSerializer(serializers.ModelSerializer):
    num_of_items = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ["id", "cart_code", "num_of_items"]
        
    def get_num_of_items(self, cart):
        num_of_items = sum([item.quantity for item in cart.items.all()])
        return num_of_items
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email']
        
        
 
        
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']

class OrdersSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status = serializers.StringRelatedField()
    class Meta:
        model = Orders
        fields = ['id', 'order_code', 'status', 'info', 'date', 'amount', 'items']