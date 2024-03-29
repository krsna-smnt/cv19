from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('india/', views.india, name='india'),
    path('research/', views.research, name='research'),
    path('datasets/', views.datasets, name='datasets'),
    path('about/', views.about, name='about'),
    path('viewfeedback', views.viewfeedback, name='viewfeedback'),
    path('userTracking/', views.userTracking, name='userTracking'),
]