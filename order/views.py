from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from .models import Order, OrderItem, Product
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework import viewsets
from .models import Order, OrderItem
from .serializers import OrderItemSerializer, OrderSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        order_items_data = request.data.pop('order_items')
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            
            for order_item_data in order_items_data:
                product_id = order_item_data.pop('product')  # Remove 'product' from order_item_data
                product = Product.objects.get(id=product_id)  # Fetch the Product instance
                OrderItem.objects.create(order=serializer.instance, product=product, **order_item_data)
            
            headers = self.get_success_headers(serializer.data)
            return JsonResponse("Success",safe=False)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def my_order(self, request):
        try:
            order = Order.objects.filter(user=request.user)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({'error': 'order not found for the logged-in user.'})
    
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]