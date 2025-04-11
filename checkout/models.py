from django.db import models

class ItemOffer(models.Model):
    item = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # Storing in dollars
    no_of_units_for_offer = models.PositiveIntegerField()
    special_price_on_offer = models.DecimalField(max_digits=10, decimal_places=2)  # Storing in dollars
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item} - {self.no_of_units_for_offer} for ${self.special_price_on_offer}"

    class Meta:
        verbose_name = "Item Offer"
        verbose_name_plural = "Item Offers"