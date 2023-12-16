from django import template

register = template.Library()


@register.filter(name='get')
def get(dictionary, key):
    return dictionary.get(key, '')
