from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.conf import settings
from .models import *

# Create your views here.

# def dochange(request):
# 	subregions = Subregion.objects.all()

# 	f = open(settings.MEDIA_ROOT + "dist_codes.txt")
# 	lst = f.readlines()
# 	for l in lst:
# 		wi = l.split(' ')
# 		w = [th.rstrip('\n') for th in wi]

# 		c = w[-1]
# 		sb = ""
# 		for i in w:
# 			if i == w[-1]:
# 				continue

# 			sb += i
# 			if i != w[-2]:
# 				sb += " "

# 		try:
# 			subregion = subregions.get(name=sb)
# 			subregion.code = c
# 			subregion.save()
# 		except:
# 			print(c, sb)


def home(request):
	countries = Country.objects.all()
	world = countries.get(name='World')
	percentage = round(100 * world.new_infected / world.total_cases, 2)

	max_cases = countries.exclude(name='World').order_by('-total_cases')[0].total_cases
	min_cases = countries.exclude(name='World').order_by('total_cases')[0].total_cases
	
	return render(request, 'website/home.html', {'countries': countries, 'world': world, 'percentage': percentage, 'max_cases': max_cases, 'min_cases': min_cases})


def india(request):
	countries = Country.objects.all()
	subregions = Subregion.objects.all()
	india = Country.objects.get(name='India')

	max_cases = subregions.order_by('-total_cases')[0].total_cases
	min_cases = subregions.order_by('total_cases')[0].total_cases

	return render(request, 'website/india.html', {'subregions': subregions, 'india': india, 'max_cases': max_cases, 'min_cases': min_cases})


def datasets(request):
	return render(request, 'website/datasets.html', {})


def research(request):
	sources = ['arxiv']
	if request.method == 'POST':
		source = request.POST['sources']
		sources = source.split('#')

	papers = []
	if 'arxiv' not in sources:
		f = open(settings.MEDIA_ROOT + "pubs_latest.csv", encoding='utf-8')
		lst = f.readlines()

		for item in lst:
			row = []
			done = False

			for thing in item.split("\""):
				if len(thing) > 3:
					done = True
					thing = thing.lstrip(',').rstrip(',')
					row.append(thing)

			if done:
				try:
					if "medrxiv" in row[2] and "medrxiv" in sources:
						row.append("medrxiv")
						papers.append(row)
					elif "biorxiv" in row[2] and "biorxiv" in sources:
						row.append("biorxiv")
						papers.append(row)
				except IndexError:
					papers.append(row)
	else:
		f = open(settings.MEDIA_ROOT + "pubs_arxiv_latest.csv", encoding='utf-8')
		lst = f.readlines()

		for item in lst:
			row = []
			done = False

			for thing in item.split("\""):
				if len(thing) > 6:
					done = True
					thing = thing.lstrip(',').rstrip(',')

					if "http" in thing:
						things = thing.split(',')
						for th in things:
							row.append(th)
					else:
						row.append(thing)

			if done:
				row.insert(3, "arxiv")
				papers.append(row)

	selled = ""
	for item in sources:
		selled += item
	return render(request, 'website/research.html', {'papers': papers, 'selled': selled})


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

	file.close()


def saveSubregionStats(file):
	file.open()
	lst = file.readlines()

	subregions = Subregion.objects.all()
	for line in lst:
		vals = line.decode("utf-8").split(',')

		try:
			subregion = subregions.get(name=vals[0].strip())
		except:
			subregion = Subregion()

		subregion.name = vals[0].strip()
		subregion.total_cases = vals[1].strip()
		subregion.dead = vals[2].strip()
		subregion.save()

	file.close()


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
		afile.content = "color"
		afile.file = colorIndia
		afile.save()

		saveSubregions(afile.file)

		afile = Afile()
		afile.region = "india"
		afile.content = "stats"
		afile.file = statsIndia
		afile.save()

		saveSubregionStats(afile.file)

		return HttpResponse("Files Uploaded and Data Updated.")
