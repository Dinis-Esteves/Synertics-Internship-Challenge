from django.db import models

# Create your models here.

class FuturesPrice(models.Model):
    date = models.DateField()
    product_name = models.CharField(max_length=20)  # e.g., "GREBY26"
    average_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} on {self.date}"