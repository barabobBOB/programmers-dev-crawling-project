from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
        
    class Meta:
        abstract: bool = True
        

class CoinSymbol(Timestamp):
    in_sync = models.BooleanField()
    coin_symbol = models.CharField(max_length=10, unique=True, verbose_name="coin_symbol")
    
    class Meta:
        verbose_name = _("CoinSymbol")
        verbose_name_plural = _("CoinSymbols")

    def __str__(self) -> str:
        return self.coin_symbol

    def get_absolute_url(self) -> str:
        return reverse("CoinSymbol_detail", kwargs={"pk": self.pk})


class CoinPriceAllChartMarket(Timestamp):
    coin_symbol = models.ForeignKey(CoinSymbol, verbose_name=_("coin_symbol_fore"), on_delete=models.CASCADE)
    price = models.FloatField(verbose_name="price")
    trade_timestamp = models.DateField(verbose_name="all_coin_trade_time")         

    class Meta:
        verbose_name = _("CoinPriceAllChartMarket")
        verbose_name_plural = _("CoinPriceAllChartMarkets")

    def __str__(self):
        return self.coin_symbol

    def get_absolute_url(self):
        return reverse("CoinPriceAllChartMarket_detail", kwargs={"pk": self.pk})