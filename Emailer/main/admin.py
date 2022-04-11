from django import forms
from django.contrib import admin

# Register your models here.
from Emailer.main.models import CustomTemplate


class ContentCreatorsForm(forms.ModelForm):
    class Meta:
        model = CustomTemplate
        fields = "__all__"


class GroupContentCreators(admin.ModelAdmin):
    form = ContentCreatorsForm


admin.site.register(CustomTemplate, GroupContentCreators)
