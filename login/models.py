# W pliku models.py

from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    sex = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # W rzeczywistości, hasła powinny być przechowywane w sposób bezpieczny, np. używając hashowania

    def __str__(self):
        return self.first_name
