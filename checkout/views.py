from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ItemOffer
from .serializers import ItemOfferSerializer
from django.shortcuts import get_object_or_404

class ItemOfferAPIView(APIView):
    """
       API endpoint for managing item offers (special pricing deals).

       Provides CRUD operations for ItemOffer model:
       - Create new offers
       - Retrieve single or all offers
       - Delete existing offers

       Example requests:
       - POST /api/offers/ {item: 1, unit_price: 10.99, ...}
       - GET /api/offers/ (list all)
       - GET /api/offers/1/ (get single)
       - DELETE /api/offers/1/ (remove offer)

       Basically we are adding,getting and deleting the product
       """
    def post(self, request, format=None):
        # Convert frontend data to match model fields
        print("reques data in post:", request.data)

        data = {
             'item': request.data.get('item'),
            'unit_price': float(request.data.get('unit_price')),
            'no_of_units_for_offer': request.data.get('no_of_units_for_offer'),
            'special_price_on_offer': float(request.data.get('special_price_on_offer'))
        }
        serializer = ItemOfferSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, format=None):
        if pk:  # If primary key is provided, return single item
            item_offer = get_object_or_404(ItemOffer, pk=pk)
            serializer = ItemOfferSerializer(item_offer)
            return Response(serializer.data)
        else:  # If no primary key, return all items
            item_offers = ItemOffer.objects.all()
            serializer = ItemOfferSerializer(item_offers, many=True)  # many=True goes to serializer, not model
            return Response(serializer.data)

    def delete(self, request, pk, format=None):
        item_offer = get_object_or_404(ItemOffer, pk=pk)
        item_offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)