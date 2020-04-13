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
	cases_per_million = models.FloatField(default=0.0)
	dead_per_million = models.FloatField(default=0.0)
	first_case_date = models.CharField(max_length=50, null=True, blank=True)
	dead_color = models.CharField(max_length=7, null=True, blank=True)
	infected_color = models.CharField(max_length=7, null=True, blank=True)
	percentage_increase = models.FloatField(null=True, blank=True)
	total_tested = models.IntegerField(default=None)
	tested_per_million = models.IntegerField(default=None)


	def __str__(self):
		return self.name


class Subregion(models.Model):
	country = models.ForeignKey(Country, on_delete=models.CASCADE)
	code = models.CharField(max_length=10, null=True, blank=True)
	name = models.CharField(max_length=200)
	population = models.IntegerField(default=0)
	total_cases = models.IntegerField(default=0)
	infected = models.IntegerField(default=0)
	dead = models.IntegerField(default=0)
	cured = models.IntegerField(default=0)
	first_case_date = models.CharField(max_length=50, null=True, blank=True)
	dead_color = models.CharField(max_length=7, null=True, blank=True)
	infected_color = models.CharField(max_length=7, null=True, blank=True)
	percentage_increase = models.FloatField(null=True, blank=True)

	def __str__(self):
		return self.name


class Afile(models.Model):
	region = models.CharField(max_length=10) # india or world
	content = models.CharField(max_length=10) # colors or stats
	file = models.FileField()

	def __str__(self):
		return self.region + " - " + self.content


class Feedback(models.Model):
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.id)


class UserTracking(models.Model):
	ip_address = models.CharField(null=True, blank=True, max_length=50)
	count = models.IntegerField(null=True, blank=True)
	country = models.CharField(null=True, blank=True, max_length=50)
	latitude = models.FloatField(null=True, blank=True)
	longitude = models.FloatField(null=True, blank=True)
	timezone = models.CharField(null=True, blank=True, max_length=50)
	organization = models.CharField(null=True, blank=True, max_length=500)
	city = models.CharField(null=True, blank=True, max_length=100)
	country_code = models.CharField(null=True, blank=True, max_length=10)
	region = models.CharField(null=True, blank=True, max_length=100)
	postal = models.CharField(null=True, blank=True, max_length=10)

	def __str__(self):
		return self.ip_address


class Publication(models.Model):
	title = models.CharField(max_length=1000, null=True, blank=True)
	authors = models.CharField(max_length=1000, null=True, blank=True)
	link = models.CharField(max_length=500, null=True, blank=True)
	source = models.CharField(max_length=10, null=True, blank=True)
	pdf = models.CharField(max_length=500, null=True, blank=True)
	date = models.CharField(max_length=400, null=True, blank=True)
	comments = models.CharField(max_length=1000, null=True, blank=True)

	def __str__(self):
		return self.title