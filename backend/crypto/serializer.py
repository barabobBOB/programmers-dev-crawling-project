from rest_framework import serializers
from django_filters import rest_framework

from typing import *
from .models import *


class CoinTradingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinPriceAllChartMarket
        fields = "__all__"


class CoinListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinSymbol
        fields = ["coin_symbol"]


# Filter
class UpperCaseFilter(rest_framework.CharFilter):
    def filter(self, qs: str, value: str) -> str:
        if value:
            value: str = value.upper()
        return super().filter(qs, value)

class CoinListUpperFilter(rest_framework.FilterSet):
    coin_symbol = UpperCaseFilter(lookup_expr="icontains")

    class Meta:
        model = None
        fields = None


