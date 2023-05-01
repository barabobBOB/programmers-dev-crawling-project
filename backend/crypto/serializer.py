from rest_framework import serializers
from .models import * 



class CoinSymbolSerializer(serializers.ModelSerializer):
    sync = serializers.BooleanField()
    
    class Meta:
        model = CoinSymbol
        fields = ["sync"]
    
    
