from django.shortcuts import render
from . models import WalletTransaction

# Create your views here.
def wallet(request):
    transactions = WalletTransaction.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user/wallet.html', {'transactions': transactions})