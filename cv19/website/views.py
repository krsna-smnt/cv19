from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from .models import *

# Create your views here.

def home(request):
	return render(request, 'website/home.html', {})