from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('saveCountries/', views.saveCountries, name='saveCountries'),
    path('saveSubregions/', views.saveSubregions, name='saveSubregions'),
    path('saveCountryCodes/', views.saveCountryCodes, name='saveCountryCodes'),
]