from django.shortcuts import render
from . models import Referral, WalletTransaction
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Order, ReturnRequest
from django.db.models import F
from django.db import transaction
from django.contrib.auth.decorators import login_required

# Create your views here.
def my_wallet(request):
    user = request.user
    transactions = WalletTransaction.objects.filter(user=user).order_by('-created_at')
    
    context = {
        'wallet_balance': user.wallet,  # Assuming `wallet` is a field on your `Account` model
        'transactions': transactions,
    }
    
    return render(request, 'user/my_wallet.html',context)



def request_return(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    if order.status == 'Delivered' and not hasattr(order, 'return_request'):
        # Create a return request
        ReturnRequest.objects.create(order=order, reason=request.POST.get('reason', 'No reason provided'))

        messages.success(request, 'Return request has been submitted.')
    else:
        messages.error(request, 'Return requests can only be made for delivered orders or a request already exists.')

    return redirect('order_detail', order_number=order_number)

def admin_confirm_return(request, return_request_id):
    return_request = get_object_or_404(ReturnRequest, id=return_request_id)
    order = return_request.order

    if return_request.status == 'Requested':
        # Start a transaction to ensure atomic operations
        with transaction.atomic():
            # Confirm the return request
            return_request.status = 'Confirmed'
            return_request.save()

            # Update order status
            order.status = 'Returned'
            order.save()

            # Get the user associated with the order
            user = order.user

            if user:
                # Credit the wallet
                user.wallet += order.grand_total
                user.save()

                # Record the wallet transaction
                WalletTransaction.objects.create(
                    user=user,
                    amount=order.grand_total,
                    transaction_type='Credit',
                    description=f'Refund for order {order.order_number}'
                )

                # Update product quantities
                for item in order.items.all():
                    product = item.product
                    product.quantity += item.quantity
                    product.save()

                # Show success message
                messages.success(request, 'Return request confirmed, wallet credited, and product quantities updated.', extra_tags='order_detail')
            else:
                messages.error(request, 'User does not exist.', extra_tags='order_detail')

    else:
        messages.error(request, 'Return request cannot be confirmed.', extra_tags='order_detail')

    return redirect('admin_side/admin_return_requests.html', order_number=order.order_number)

def admin_reject_return(request, return_request_id):
    return_request = get_object_or_404(ReturnRequest, id=return_request_id)

    if return_request.status == 'Requested':
        # Reject the return request
        return_request.status = 'Rejected'
        return_request.save()

        messages.success(request, 'Return request rejected.')
    else:
        messages.error(request, 'Return request cannot be rejected.')

    return redirect('admin_return_requests')

def admin_return_requests(request):
    return_requests = ReturnRequest.objects.all()
    return render(request, 'admin_side/admin_return_requests.html', {'return_requests': return_requests})


@login_required
def referral_page(request):
    referral = get_object_or_404(Referral, user=request.user)
    friends = referral.referred_friends.all()

    context = {
        'referral_code': referral.referral_code,
        'friends': friends,
    }
    return render(request, 'user/referral.html', context)