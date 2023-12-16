from django import template

register = template.Library()


@register.filter(name='get')
def cut(dictionary, key):
    return dictionary.get(key, '')
