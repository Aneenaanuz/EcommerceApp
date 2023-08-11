
from django.db import models
from myaccount.models import User
from product.models import Product

# product/models.py

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name} in Order {self.order.id}"



