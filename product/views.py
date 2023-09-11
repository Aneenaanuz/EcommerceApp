
from rest_framework import viewsets,filters
from .models import Category, Product,Cart,CartItem
from .serializers import CategorySerializer, ProductSerializer,CartSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff
    

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminOrReadOnly]    

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminOrReadOnly] 

    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    @action(detail=False, methods=['get'])
    def my_cart(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found for the logged-in user.'})
        
        
    @action(detail=False, methods=['post'])
    def add_to_cart(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=404)

        # Check if the item is already in the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        # Update the quantity of the cart item
        cart_item.quantity += quantity
        cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['put'])
    def update_cart_item(self, request):
        cart_item_id = request.data.get('cart_item_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            cart_item = CartItem.objects.get(pk=cart_item_id)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found.'}, status=404)

        cart_item.quantity = quantity
        cart_item.save()

        serializer = CartSerializer(cart_item.cart)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'])
    def remove_from_cart(self, request):
        cart_item_id = request.data.get('cart_item_id')

        try:
            cart_item = CartItem.objects.get(pk=cart_item_id)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found.'}, status=404)

        cart_item.delete()

        serializer = CartSerializer(cart_item.cart)
        return Response(serializer.data)
    
