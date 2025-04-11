from django.urls import path
from .views import ItemOfferAPIView

urlpatterns = [
    # For listing all items and creating new items
    path('product/', ItemOfferAPIView.as_view(), name='item-offers-list'),

    # For retrieving, updating, or deleting a specific item
    path('product/<int:pk>/', ItemOfferAPIView.as_view(), name='item-offers-detail'),
]