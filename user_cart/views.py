from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserCart
from .serializers import UserCartSerializer
from django.shortcuts import get_object_or_404
from .utils import checkout_calculation


class UserCartAPIView(APIView):
    def get(self, request, user_id=None, format=None):
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

    def put(self, request, format=None):
        user_id = request.data.get('user_id')
        item_id = request.data.get('item_id')

        try:
            cart_item = UserCart.objects.get(user_id=user_id, item_id=item_id)
        except UserCart.DoesNotExist:
            return Response({"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)

        # Update only the fields that are provided
        if 'quantity' in request.data:
            cart_item.quantity = request.data['quantity']
        if 'unit_price' in request.data:
            cart_item.unit_price = request.data['unit_price']
        # Add other fields as needed

        cart_item.save()
        serializer = UserCartSerializer(cart_item)
        return Response(serializer.data)

    def delete(self, request, format=None):
        user_id = request.data.get('user_id')
        item_id = request.data.get('item_id')

        try:
            cart_item = UserCart.objects.get(user_id=user_id, item_id=item_id)
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserCart.DoesNotExist:
            return Response({"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)