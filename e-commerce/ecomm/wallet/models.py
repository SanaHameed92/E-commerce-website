from django.db import models
from accounts.models import Account
from products.models import Order

# Create your models here.
class WalletTransaction(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=(('Credit', 'Credit'), ('Debit', 'Debit')))
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f'{self.transaction_type} - {self.amount} for {self.user.email}'
    

class ReturnRequest(models.Model):
    STATUS_CHOICES = (
        ('Requested', 'Requested'),
        ('Confirmed', 'Confirmed'),
        ('Rejected', 'Rejected'),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='return_request')
    
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Requested')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Return Request for Order {self.order.order_number}'