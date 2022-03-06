from django import template

register = template.Library()


@register.filter(name="filter")
def selected_labels(form):
    return [(value, label) for field in form.fields for value, label in form.fields[field].choices]
