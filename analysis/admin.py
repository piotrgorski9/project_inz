from django.contrib import admin
from .models import Country, Emigration

class CountryAdmin(admin.ModelAdmin):
    list_display = ('country', 'capital', 'area', 'population', 'phone_code', 'continent', 'flag_path')

class EmigrationAdmin(admin.ModelAdmin):
    list_display = ('country', 'year', 'number_of_emigrants')

admin.site.register(Country, CountryAdmin)
admin.site.register(Emigration, EmigrationAdmin)
