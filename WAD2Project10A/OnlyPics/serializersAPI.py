from rest_framework import serializers
from .models import Price

class PriceModelSerializer(serializers.ModelSerializer):
     class Meta:
         model = Price
         fields = [
             'type',
             'name',
             'product',
             'value',
         ]