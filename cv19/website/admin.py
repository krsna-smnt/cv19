from django.contrib import admin
from website.models import Country, Subregion, Afile

# Register your models here.

admin.site.register(Country)
admin.site.register(Subregion)
admin.site.register(Afile)