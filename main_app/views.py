from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

# Create your views here.

# Base views
def home(request):
    return render(request, 'home.html')
