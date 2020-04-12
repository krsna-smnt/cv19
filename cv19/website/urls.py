from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('india/', views.india, name='india'),
    path('saveCountries/', views.saveCountries, name='saveCountries'),
    path('saveSubregions/', views.saveSubregions, name='saveSubregions'),
    path('saveCountryCodes/', views.saveCountryCodes, name='saveCountryCodes'),
    path('saveCountryStats/', views.saveCountryStats, name='saveCountryStats'),
    path('saveSubregionStats/', views.saveSubregionStats, name='saveSubregionStats'),
    path('uploadFiles/', views.uploadFiles, name='uploadFiles'),
    path('research/', views.research, name='research'),
    path('datasets/', views.datasets, name='datasets'),
    path('about/', views.about, name='about'),
    path('viewfeedback', views.viewfeedback, name='viewfeedback'),
    # path('dochange/', views.dochange, name='dochange'),
]