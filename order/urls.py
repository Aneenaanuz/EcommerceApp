from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderItemViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'orderItem', OrderItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]