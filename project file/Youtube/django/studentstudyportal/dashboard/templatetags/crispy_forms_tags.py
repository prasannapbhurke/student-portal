from django import template

register = template.Library()


@register.filter
def crispy(form):
    return form.as_p()
