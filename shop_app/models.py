from django.db import models
from django.utils.text import slugify
from django.conf import settings

# from IRBackend import settings


class Category(models.Model):
    category_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.category_name
        
class Genres(models.Model):
    genre_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.genre_name

class Products(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)
    image = models.ImageField(upload_to="img")
    descr = models.TextField(max_length=999)
    price = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        
        if not self.slug:
            self.slug = slugify(self.title)
            unique_slug = self.slug
            counter = 1 
            if Products.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{self.slug} - {counter}'
                counter += 1 
            self.slug = unique_slug
            
        super().save(*args, **kwargs)
    
class Artists(models.Model):
    artist_name = models.CharField(max_length=50)
    image =  models.ImageField(upload_to="img")
    destination = models.CharField(max_length=50)
    
    def __str__(self):
        return self.artist_name 
    
class Cart(models.Model):
    cart_code = models.CharField(max_length=11, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return self.cart_code
    
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__ (self):
        return f"{self.quantity} x {self.product.title} in cart {self.cart.id}"
    
class Statuses(models.Model):
    status_name = models.CharField(max_length=50)    
    
    def __str__ (self):
        return self.status_name

class Orders(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.ForeignKey(Statuses, on_delete=models.CASCADE, default=1)
    order_code = models.CharField(max_length=7, unique=True)
    info = models.TextField(max_length=700)
    date = models.DateField(auto_now_add=True,blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    amount = models.IntegerField(default=0)
    
    def __str__(self):
        return self.order_code
    
class OrderItem(models.Model):
    order = models.ForeignKey(Orders, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__ (self):
        return f"{self.quantity} x {self.product.title} in cart {self.order.order_code}"