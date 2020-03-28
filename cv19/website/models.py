from django.db import models

# Create your models here.

class Country(models.Model):
	name = models.CharField(max_length=200)
	code = models.CharField(max_length=10, null=True, blank=True)
	population = models.IntegerField(default=0)
	total_cases = models.IntegerField(default=0)
	new_infected = models.IntegerField(default=0)
	infected = models.IntegerField(default=0)
	new_dead = models.IntegerField(default=0)
	dead = models.IntegerField(default=0)
	cured = models.IntegerField(default=0)
	critical = models.IntegerField(default=0)
	cases_per_million = models.IntegerField(default=0)
	dead_per_million = models.IntegerField(default=0)
	first_case_date = models.DateField(null=True, blank=True)
	dead_color = models.CharField(max_length=7, null=True, blank=True)
	infected_color = models.CharField(max_length=7, null=True, blank=True)

	def __str__(self):
		return self.name


class Subregion(models.Model):
	country = models.ForeignKey(Country, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	population = models.IntegerField(default=0)
	total_cases = models.IntegerField(default=0)
	infected = models.IntegerField(default=0)
	dead = models.IntegerField(default=0)
	cured = models.IntegerField(default=0)
	first_case_date = models.DateField(null=True, blank=True)
	dead_color = models.CharField(max_length=7, null=True, blank=True)
	infected_color = models.CharField(max_length=7, null=True, blank=True)

	def __str__(self):
		return self.name
