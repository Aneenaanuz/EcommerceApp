
from rest_framework import serializers
from .models import Order, OrderItem
from product.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # You can use your existing ProductSerializer
    
    class Meta:
        model = OrderItem
        fields = ['id', 'quantity', 'product']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True,read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'order_items', 'created_at']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)

        for order_item_data in order_items_data:
            OrderItem.objects.create(order=order, **order_item_data)

        return order

