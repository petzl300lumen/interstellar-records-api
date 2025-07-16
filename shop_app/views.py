from django.shortcuts import render
import random
from rest_framework.decorators import api_view, permission_classes
from .models import *
from .serializers import *
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.conf import settings
BASE_URL = settings.REACT_BASE_URL


@api_view(['GET'])
def products(request):
    products = Products.objects.all()
    serializer = ProductsSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def artists(request):
    artists = Artists.objects.all()
    serializer = ArtistSerializer(artists, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def genres(request):
    genres = Genres.objects.all()
    serializer = GenresSerializer(genres, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def category(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, slug):
    product = Products.objects.get(slug=slug)
    serializer = DetailedProductSerializer(product)
    return Response(serializer.data)

@api_view(['POST'])
def add_item(request):
    try:
        cart_code = request.data.get("cart_code")
        product_id = request.data.get("product_id")
        cart, created = Cart.objects.get_or_create(cart_code=cart_code)
        product = Products.objects.get(id=product_id)
        cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cartitem.quantity = 1
        cartitem.save()
        serializer = CartItemSerializer(cartitem)
        return Response({"data": serializer.data, "message": "Cart created"}, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
@api_view(['GET'])
def product_in_cart(request):
    cart_code = request.query_params.get("cart_code")
    product_id = request.query_params.get("product_id")
    
    cart = Cart.objects.get(cart_code=cart_code)
    product = Products.objects.get(id=product_id)
    
    product_exists_in_cart = CartItem.objects.filter(cart=cart, product=product).exists()
    return Response({'product_in_cart': product_exists_in_cart})

@api_view(['GET'])
def get_cart_stat(request):
    cart_code = request.query_params.get("cart_code")
    cart = Cart.objects.get(cart_code=cart_code, paid=False)
    serializer = SimpleCartSerializer(cart)
    return Response(serializer.data)

@api_view(['GET'])
def get_cart(request):
    cart_code = request.query_params.get("cart_code")
    cart = Cart.objects.get(cart_code=cart_code, paid=False)
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(['PATCH'])
def upadate_quantity(request):
    try:
        cartitem_id = request.data.get("item_id")
        quantity = request.data.get("quantity")
        quantity = int(quantity)
        cartitem = CartItem.objects.get(id=cartitem_id)
        cartitem.quantity = quantity
        cartitem.save()
        serializer = CartItemSerializer(cartitem)
        return Response({'data': serializer.data, "message": "Quantity updated!"})        
    except Exception as e:
        return Response({'error': str(e)}, status=400)
    
@api_view(['POST'])
def delete_cartitem(request):
    cartitem_id = request.data.get("item_id")
    cartitem = CartItem.objects.get(id=cartitem_id)
    cartitem.delete()
    return Response({'message': 'deleted'}, status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not password or not email:
            return Response({'error': 'Все поля обязательны'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Пользователь с таким именем уже существует'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({'message': 'Пользователь успешно зарегистрирован'}, status=status.HTTP_201_CREATED)
    
    
    # Баганная функция заказа
"""
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    user = request.user
    cart_code = request.data.get("cart_code")
    info = request.data.get("info", "")
    cart = Cart.objects.get(cart_code=cart_code, paid=False)
    status = Statuses.objects.get(pk=1)  # "Сформирован" по умолчанию

    user_id = user.id if user else 0
    rand_digits = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    order_code = f"{user_id}-{rand_digits}"

    amount = sum([item.product.price * item.quantity for item in cart.items.all()])

    order = Orders.objects.create(
        user=user,
        status=status,
        order_code=order_code,
        info=info,
        amount=amount
    )

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity
        )

    cart.items.all().delete()
    cart.paid = True
    cart.save()

    return Response({'message': 'Заказ оформлен', 'order_code': order_code}, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_history(request):
    orders = Orders.objects.filter(user=request.user).order_by('-date')
    serializer = OrdersSerializer(orders, many=True)
    return Response(serializer.data)
    
    """