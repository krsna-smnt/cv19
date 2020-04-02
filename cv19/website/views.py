from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.conf import settings
from .models import *

# Create your views here.

def home(request):
	countries = Country.objects.all()
	world = countries.get(name='World')
	percentage = round(100 * world.new_infected / world.total_cases, 2)
	return render(request, 'website/home.html', {'countries': countries, 'world': world, 'percentage': percentage})


def saveCountries(file):
	file.open()
	for line in file.readlines():
		lst = line.decode("utf-8").split(',')

		try:
			country = Country.objects.get(name=lst[0])
		except:
			country = Country()

		country.name, country.infected_color, country.dead_color = lst[0], lst[1], lst[2]
		country.save()

	file.close()
	# return HttpResponse("Countries Saved")


def saveSubregions(file):
	file.open()

	for line in file.readlines():
		lst = line.decode("utf-8").split(',')

		try:
			subregion = Subregion.objects.get(name=lst[0])
		except:
			subregion = Subregion()

		subregion.name, subregion.infected_color, subregion.dead_color = lst[0], lst[1], lst[2]
		subregion.country = Country.objects.get(name='India')
		subregion.save()

	file.close()

	# return HttpResponse("Subregions Saved")


def saveCountryCodes(request):
	f = open(settings.MEDIA_ROOT + "CountryCodes.txt")
	lst = f.readlines()

	countries = Country.objects.all()
	for i in range(0, len(lst), 2):
		try:
			country = countries.get(name=lst[i].strip())
			country.code = lst[i+1]
			country.save()
		except:
			print("Not Found")


#name,total_cases,new_cases,total_dead,new_dead,total_cured,active_cases,critical_cases,cases_per_mil,deaths_per_mil,date
def saveCountryStats(file):
	file.open()
	lst = file.readlines()

	countries = Country.objects.all()
	for line in lst:
		vals = line.decode("utf-8").split(',')

		try:
			country = countries.get(name=vals[0].strip())
		except:
			country = Country()

		country.name = vals[0].strip()

		oldn = country.total_cases
		newn = vals[1].strip()

		country.total_cases = vals[1].strip()
		country.new_infected = vals[2].strip()
		country.infected = vals[6].strip()
		country.new_dead = vals[4].strip()
		country.dead = vals[3].strip()
		country.cured = vals[5].strip()
		country.critical = vals[7].strip()
		country.cases_per_million = vals[8].strip()
		country.dead_per_million = vals[9].strip()

		try:
			if oldn != newn:
				country.percentage_increase = round(100 * int(country.new_infected) / int(country.total_cases), 2)
		except ZeroDivisionError:
			country.percentage_increase = None
		country.save()

#		except Exception as e:
#			print(e)

	file.close()
	# return HttpResponse("Stats Saved")


def saveSubregionStats(file):
	file.open()
	lst = f.readlines()

	subregions = Subregion.objects.all()
	for line in lst:
		vals = line.decode("utf-8").split(',')

		try:
			subregion = subregions.get(name=vals[0].strip())
			subregion.total_cases = vals[1].strip()
			subregion.dead = vals[2].strip()
			subregion.save()

		except Exception as e:
			print(e)

	file.close()
	# return HttpResponse("Stats Saved")


def uploadFiles(request):
	if request.method == 'GET':
		return render(request, 'website/uploadFiles.html', {})
	elif request.method == 'POST':
		statsIndia = request.FILES['statsIndia']
		statsWorld = request.FILES['statsWorld']
		colorWorld = request.FILES['colorWorld']
		colorIndia = request.FILES['colorIndia']

		afile = Afile()
		afile.region = "world"
		afile.content = "color"
		afile.file = colorWorld
		afile.save()
		saveCountries(afile.file)


		afile = Afile()
		afile.region = "world"
		afile.content = "stats"
		afile.file = statsWorld
		afile.save()

		saveCountryStats(afile.file)

		afile = Afile()
		afile.region = "india"
		afile.content = "stats"
		afile.file = statsIndia
		afile.save()

		afile = Afile()
		afile.region = "india"
		afile.content = "color"
		afile.file = colorIndia
		afile.save()

		return HttpResponse("Files Uploaded and Data Updated.")
