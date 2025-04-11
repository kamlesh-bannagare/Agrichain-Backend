from django.urls import path
from .views import UserCartAPIView

urlpatterns = [
    path('cart/', UserCartAPIView.as_view(), name='user-cart'),
    path('cart/<int:user_id>/', UserCartAPIView.as_view(), name='user-cart-detail'),
]