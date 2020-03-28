from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.conf import settings
from .models import *

# Create your views here.

def home(request):
	countries = Country.objects.all()
	return render(request, 'website/home.html', {'countries': countries})


def saveCountries(request):
	f = open(settings.MEDIA_ROOT + "color_codes_World_27-Mar-2020_23:41.csv")

	for line in f.readlines():
		lst = line.split(',')

		try:
			country = Country.objects.get(name=lst[0])
		except:
			country = Country()

		country.name, country.infected_color, country.dead_color = lst[0], lst[1], lst[2]
		country.save()

	return HttpResponse("Countries Saved")


def saveSubregions(request):
	f = open(settings.MEDIA_ROOT + "color_codes_India_27-Mar-2020_23:42.csv")

	for line in f.readlines():
		lst = line.split(',')

		try:
			subregion = Subregion.objects.get(name=lst[0])
		except:
			subregion = Subregion()

		subregion.name, subregion.infected_color, subregion.dead_color = lst[0], lst[1], lst[2]
		subregion.country = Country.objects.get(name='India')
		subregion.save()

	return HttpResponse("Subregions Saved")


def saveCountryCodes(request):
	f = open(settings.MEDIA_ROOT + "CountryCodes.txt")
	lst = f.readlines()

	countries = Country.objects.all()
	for i in range(0, len(lst), 2):
		try:
			country = countries.get(name=lst[i].strip())
			country.code = lst[i+1]
			country.save()
			print(country, country.code)
		except:
			print("Not Found")
