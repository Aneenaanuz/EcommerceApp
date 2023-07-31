# accounts/urls.py
from django.urls import path
from .views import UserRegistration
from .views import UserLogin,TokenRefresh

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user-registration'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('token/refresh/', TokenRefresh.as_view(), name='token-refresh')
]