from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.conf import settings
from .models import *
import random

# Create your views here.

def userTracking(request):
	users = UserTracking.objects.all()
	return render(request, 'website/userTracking.html', {'users': users})


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

	papers = Publication.objects.filter(source__in=sources)

	selled = ""
	for item in sources:
		selled += item

	return render(request, 'website/research.html', {'papers': papers, 'selled': selled})


def about(request):
	makers = [['Abhay', 'https://github.com/abyswp/', 'abyswp'], ['Sumanth', 'https://github.com/krsna-smnt/', 'krsna-smnt']]
	i = random.choice([1, 2])

	if i == 2:
		makers.reverse()

	if request.method == 'GET':
		return render(request, 'website/about.html', {'makers': makers})
	else:
		feedback = Feedback()
		feedback.content = request.POST['content']
		feedback.save()

		return render(request, 'website/about.html', {'feedback': 'filled', 'makers': makers})


def viewfeedback(request):
	feedbacks = Feedback.objects.all().order_by('-timestamp')
	return render(request, 'website/viewfeedback.html', {'feedbacks': feedbacks, 'feedback': feedbacks})
