from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.conf import settings
from .models import *

# Create your views here.

def home(request):
	countries = Country.objects.all()
	return render(request, 'website/home.html', {'countries': countries})


def saveCountries(request):
	f = open(settings.MEDIA_ROOT + "color_codes_World_28-Mar-2020_15:11.csv")

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
	f = open(settings.MEDIA_ROOT + "color_codes_India_28-Mar-2020_15:06.csv")

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


#name,total_cases,new_cases,total_dead,new_dead,total_cured,active_cases,critical_cases,cases_per_mil,deaths_per_mil,date
def saveCountryStats(request):
	f = open(settings.MEDIA_ROOT + "datasets_World_28-Mar-2020_15:11.csv")
	lst = f.readlines()

	countries = Country.objects.all()
	for line in lst:
		vals = line.split(',')

		try:
			country = countries.get(name=vals[0].strip())
			country.total_cases = vals[1].strip()
			country.new_infected = vals[2].strip()
			country.infected = vals[6].strip()
			country.new_dead = vals[4].strip()
			country.dead = vals[3].strip()
			country.cured = vals[5].strip()
			country.critical = vals[7].strip()
			country.cases_per_million = vals[8].strip()
			country.dead_per_million = vals[9].strip()
			country.first_case_date = vals[10].strip()
			country.save()

			print(country.name)
		except Exception as e:
			print(e)
			print(vals[0].strip() + " not done")

	return HttpResponse("Stats Saved")


def saveSubregionStats(request):
	f = open(settings.MEDIA_ROOT + "datasets_India_28-Mar-2020_15:06.csv")
	lst = f.readlines()

	subregions = Subregion.objects.all()
	for line in lst:
		vals = line.split(',')

		try:
			subregion = subregions.get(name=vals[0].strip())
			subregion.total_cases = vals[1].strip()
			subregion.dead = vals[2].strip()
			subregion.save()

			print(subregion.name)
		except Exception as e:
			print(e)
			print(vals[0].strip() + " not done")

	return HttpResponse("Stats Saved")