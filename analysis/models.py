from django.db import models

class Country(models.Model):
    country = models.CharField(max_length=50)
    capital = models.CharField(max_length=50)
    area = models.IntegerField(default=0)
    population = models.IntegerField(default=0)
    phone_code = models.IntegerField(default=None, null=True)
    continent = models.CharField(max_length=50, default=None, null=True)
    flag_path = models.CharField(max_length=255, default='ścieżka_do_domyślnej_flagi')

    def __str__(self):
        return self.country

class Emigration(models.Model):
    id_emigration = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    year = models.IntegerField()
    number_of_emigrants = models.IntegerField()

    def __str__(self):
        return f"{self.country.country} - {self.year} - {self.number_of_emigrants}"

    class Meta:
        app_label = 'analysis'
