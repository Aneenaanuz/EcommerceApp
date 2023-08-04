
from rest_framework import serializers
from .models import Category, Product,Cart,CartItem

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    category = serializers.SlugRelatedField(slug_field='name',queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.CharField(read_only=True)
    class Meta:
        model = CartItem
        fields = ['id', 'quantity', 'cart', 'product']

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'
        