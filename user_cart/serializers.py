from rest_framework import serializers
from .models import UserCart

class UserCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCart
        fields = '__all__'