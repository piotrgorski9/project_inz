# models.py

from django.db import models

class Country(models.Model):
    country = models.CharField(max_length=100)
    capital = models.CharField(max_length=100)
    emigration = models.IntegerField(default=0)

    def __str__(self):
        return self.country

class OtherModel(models.Model):
    id = models.AutoField(primary_key=True)
    rok = models.IntegerField()
    liczba_osob = models.IntegerField()

    def __str__(self):
        return f"{self.rok} - {self.liczba_osob}"

    class Meta:
        app_label = 'analysis'
