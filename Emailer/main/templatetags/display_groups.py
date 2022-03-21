from django import template

from Emailer.main.models import Group

register = template.Library()


@register.simple_tag(takes_context=True)
def display_groups(context):
    return Group.objects.filter(receivers__user_id__exact=context.request.user).distinct()
