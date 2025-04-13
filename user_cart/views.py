from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserCart
from .serializers import UserCartSerializer
from django.shortcuts import get_object_or_404
from .utils import checkout_calculation


class UserCartAPIView(APIView):
    """
        API endpoint for managing user shopping carts for the checkout.

        Provides operations to:
        - Retrieve cart items with calculated totals (including special offers)
        - Add/update items in cart (auto-increments quantity if item exists)
        - Remove single items or clear entire cart

        The cart automatically handles:
        - Quantity increments when adding duplicate items
        - Special offer calculations via checkout_calculation utility
        - Bulk clearing of cart items after checkout

        Example Endpoints:
        GET    /api/cart/{user_id}/    - Get user's cart with calculated totals
        POST   /api/cart/              - Add item to cart (auto-increments if exists)
        DELETE /api/cart/{item_id}/    - Remove specific item
        DELETE /api/cart/              - Clear all items (requires user_id in body)
        """
    def get(self, request, id=None, format=None):
        user_id=id
        if user_id:
            cart_items = UserCart.objects.filter(user_id=user_id)
            serializer = UserCartSerializer(cart_items, many=True)
            cart_data_with_calculation = checkout_calculation(serializer.data)
            return Response(cart_data_with_calculation)
        return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        user_id = request.data.get('user_id')
        item_id = request.data.get('item_id')
        print("cart_data: ", request.data)
        # Check if item already exists in cart
        cart_item, created = UserCart.objects.get_or_create(
            user_id=user_id,
            item_id=item_id,
            defaults={
                'item': request.data.get('item'),
                'unit_price': request.data.get('unit_price'),
                'no_of_units_for_offer': request.data.get('no_of_units_for_offer', 0),
                'special_price_on_offer': request.data.get('special_price_on_offer', '0.00'),
                'quantity': 1
            }
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        serializer = UserCartSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    def delete(self, request, id= None, format=None):
        print("deleting the item", request.data)
        # Handle both single item deletion and clear all items after checkout
        if id is None:
            if 'user_id' in request.data:
                # This is the clear all items request
                user_id = request.data.get('user_id')
                deleted_count, _ = UserCart.objects.filter(user_id=user_id).delete()
                return Response(
                    {"message": f"Successfully deleted {deleted_count} items from cart"},
                    status=status.HTTP_204_NO_CONTENT
                )
        else:
            # This is the original single item deletion
            cart_item = get_object_or_404(UserCart, pk=id)
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)