from django import template
import re

register = template.Library()


@register.filter(name='phone')
def phone(url_path):
    try:
        pattern = re.compile(r'.*phone=(\d+).*')
        m = pattern.match(url_path)
        value = m.group(1)
    except:
        value = None
    return value
