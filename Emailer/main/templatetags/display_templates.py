from Emailer.main.models import CustomTemplate
from django import template

register = template.Library()


@register.simple_tag()
def display_templates():
    return CustomTemplate.objects.all()
