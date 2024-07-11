
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth, User
from django.contrib import messages

# Create your views here.


def index(request):
    return render(request,'index.html')







