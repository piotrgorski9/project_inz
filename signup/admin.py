from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'sex', 'email', 'user_type', 'creation_date')

admin.site.register(UserProfile, UserProfileAdmin)