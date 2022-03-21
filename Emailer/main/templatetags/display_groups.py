from django import template

from Emailer.main.models import Group, CustomTemplate

register = template.Library()


@register.simple_tag(takes_context=True)
def display_groups(context):
    return Group.objects.filter(receivers__user_id__exact=context.request.user).distinct()


@register.simple_tag(takes_context=True)
def display_templates(context):
    return [
        *CustomTemplate.objects.filter(is_global_template=True),
        *CustomTemplate.objects.filter(user=context.request.user)
    ]
