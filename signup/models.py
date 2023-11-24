from django.db import models

class UserProfile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    sex = models.CharField(max_length=10)
    email = models.EmailField(unique=True, max_length=100)
    password = models.CharField(max_length=255)
    user_type = models.CharField(max_length=20, default='normal')
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
