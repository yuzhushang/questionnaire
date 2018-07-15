from django import template

register = template.Library()


@register.filter(name='phone')
def phone(url_path):
    try:
        value = url_path.split("&")[0].split("=")[1]
    except:
        value = None
    return value
