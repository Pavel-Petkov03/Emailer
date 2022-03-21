from Emailer.main.models import CustomTemplate
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def display_templates(context):
    return CustomTemplate.objects.all()
