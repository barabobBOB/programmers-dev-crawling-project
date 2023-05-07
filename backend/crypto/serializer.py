from rest_framework import serializers
from django_filters import rest_framework

from typing import *
from .models import *


class CoinListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinSymbol
        fields = ["coin_symbol"]


class CoinPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinPriceAllChartMarket
        fields = ["coin_symbol", "price", "trade_timestamp"]
        
        
class RecentNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinnessNews
        fields = ["date", "time", "title", "content"]


class CoinNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlingInformation
        fields = ["name", "titles", "urls", "dates"]
        
        
# Filter
class UpperCaseFilter(rest_framework.CharFilter):
    def filter(self, qs: str, value: str) -> str:
        if value:
            value: str = value.upper()
        return super().filter(qs, value)


class CoinListUpperFilter(rest_framework.FilterSet):
    coin_symbol = UpperCaseFilter(lookup_expr="icontains")

    class Meta:
        model = CoinSymbol
        fields = ["coin_symbol"]
