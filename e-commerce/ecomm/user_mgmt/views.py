from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import Account
from .forms import UserCreationForm
from .forms import UserEditForm
from django.contrib import messages


# Create your views here.
def user_list(request):
    users = Account.objects.all()
    return render(request,'admin_side/user_list.html',{'users': users})


def user_delete(request, user_id):
    user = get_object_or_404(Account, id=user_id)
    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
        return redirect('user_page:user_list')
    return render(request, 'admin_side/confirm_delete_user.html', {'user': user})

    
def user_create(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_page:user_list')
    else:
        form = UserCreationForm()
    
    return render(request, 'admin_side/user_create.html', {'form': form})

def user_edit(request, user_id):
    user = get_object_or_404(Account, id=user_id)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User details updated successfully.')
            return redirect('user_page:user_list')
    else:
        form = UserEditForm(instance=user)
    
    return render(request, 'admin_side/user_edit.html', {'form': form, 'user': user})
