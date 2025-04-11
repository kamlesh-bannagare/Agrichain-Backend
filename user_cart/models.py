from django.db import models

class UserCart(models.Model):
    user_id = models.IntegerField()
    item_id = models.IntegerField()
    item = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    no_of_units_for_offer = models.IntegerField(default=0)
    special_price_on_offer = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     unique_together = ('user_id', 'item_id')  # Ensures one item per user in cart

    def __str__(self):
        return f"User {self.user_id} - {self.item} (Qty: {self.quantity})"