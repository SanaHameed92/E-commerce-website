from django.db import models
from accounts.models import Account

# Create your models here.
class WalletTransaction(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=(('Credit', 'Credit'), ('Debit', 'Debit')))
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f'{self.transaction_type} - {self.amount} for {self.user.email}'
