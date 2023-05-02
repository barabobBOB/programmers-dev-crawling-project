from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

import uuid
from typing import * 


class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
        
    class Meta:
        abstract: bool = True
    

class CoinSymbol(Timestamp):
    coin_symbol = models.CharField(max_length=10, unique=True, primary_key=True, verbose_name=_("coin_symbol"))
    coin_uuid   = models.UUIDField(unique=True, default=uuid.uuid4, verbose_name=_("coin_uuid"))
    is_sync     = models.BooleanField(default=False, verbose_name=_("coin_sync"))
    
    class Meta:
        verbose_name: str        = _("CoinSymbol")
        verbose_name_plural: str = _("CoinSymbols")
        
        indexes: List[models.Index] = [
            models.Index(
                fields=["coin_uuid", "coin_symbol"],
            )
        ]
        
    def __str__(self) -> str:
        return self.coin_symbol

    
class CoinPriceAllChartMarket(Timestamp):
    coin_symbol     = models.ForeignKey(CoinSymbol, verbose_name=_("coin_symbol_fore"), on_delete=models.CASCADE)
    price           = models.FloatField(verbose_name="price")
    trade_timestamp = models.DateField(verbose_name="all_coin_trade_time")         

    class Meta:
        verbose_name: str        = _("CoinPriceAllChartMarket")
        verbose_name_plural: str = _("CoinPriceAllChartMarkets")

    def __str__(self) -> str:
        return self.coin_symbol

