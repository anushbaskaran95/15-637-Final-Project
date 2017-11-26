from django import template
register = template.Library()


@register.filter(name='get_class')
def get_class(value):
    return value.__class__.__name__


@register.filter
def calc_time(value):
    return "{0:.1f}".format(value / 3600.0)
