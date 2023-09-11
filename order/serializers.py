from rest_framework import serializers
from .models import Order, OrderItem
from product.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # You can use your existing ProductSerializer
    
    class Meta:
        model = OrderItem
        fields = ['id', 'quantity', 'product']


class OrderSerializer(serializers.ModelSerializer):
    # Remove the 'order_items' field from here
    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at']  # Don't include 'order_items' in fields

    def create(self, validated_data):
        # order_items_data = validated_data.pop('order_items')  # Remove this line
        order = Order.objects.create(**validated_data)

        # for order_item_data in order_items_data:
        #     OrderItem.objects.create(order=order, **order_item_data)

        return order