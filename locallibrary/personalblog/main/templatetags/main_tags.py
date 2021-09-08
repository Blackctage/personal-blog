import datetime

from django import template
from django.apps import apps
from django.template.loader import get_template
from django.utils import timezone
from django.utils.timesince import timesince
from django.utils.translation import gettext as _

ArticleTypeHeader = apps.get_model('main', 'ArticleTypeHeader')

register = template.Library()


def check_number_of_time(value, time):
    if value == 1:
        return '%s %s %s' % (value, time, 'ago')
    elif value > 1:
        return '%s %s %s' % (value, time + 's', 'ago')


@register.simple_tag()
def show_algorithms():
    article_type_header = ArticleTypeHeader.objects.all()
    return article_type_header


@register.simple_tag()
def time_filter(value):
    current_time = datetime.datetime(timezone.now().year, timezone.now().month, timezone.now().day, timezone.now().hour)
    value = datetime.datetime(value.year, value.month, value.day, value.hour)

    if current_time.year - value.year >= 1:
        return check_number_of_time(current_time.year - value.year, 'year')
    elif current_time.month - value.month >= 1:
        return check_number_of_time(current_time.month - value.month, 'month')
    elif current_time.day - value.day >= 1:
        return check_number_of_time(current_time.day - value.day, 'day')
    elif current_time.hour - value.hour >= 1:
        return check_number_of_time(current_time.hour - value.hour, 'hour')
    else:
        return 'now'