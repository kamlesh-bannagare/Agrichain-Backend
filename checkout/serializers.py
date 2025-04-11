from rest_framework import serializers
from .models import ItemOffer

class ItemOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOffer
        fields = '__all__'