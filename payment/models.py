from django.db import models
from django.contrib.auth.models import User

class ShipinpAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    present_address = models.CharField(max_length=200)
    permanent_address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.CharField(max_length=200)
    country = models.CharField(max_length=200)

    #Don't make Plural form of ShipinpAddress
    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f'Shipping Address - {str(self.id)}'
    

