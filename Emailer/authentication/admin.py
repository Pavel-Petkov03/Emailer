from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AbstractUser

admin.site.register(AbstractUser, UserAdmin)