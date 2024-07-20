
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model



class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)
    email = models.EmailField(max_length=255, blank=True, null=True)

    
    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state}, {self.country} - {self.postal_code}"
    
