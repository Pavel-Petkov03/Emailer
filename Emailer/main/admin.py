from django.contrib import admin

# Register your models here.
from Emailer.main.models import CustomTemplate

admin.site.register(CustomTemplate)