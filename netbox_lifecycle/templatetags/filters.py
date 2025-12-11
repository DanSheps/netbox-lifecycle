from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


def is_expired(value):
    return value < datetime.now().date()


def expires_within_six_months(value):
    return value < (date.today() + relativedelta(months=+6))


@register.filter(is_safe=True)
def date_badge_class(value):
    if not value:
        return

    if is_expired(value):
        return mark_safe('class="badge text-bg-danger"')
    elif expires_within_six_months(value):
        return mark_safe('class="badge text-bg-warning"')
    else:
        return mark_safe('class="badge text-bg-success"')


@register.filter(is_safe=True)
def contract_status_badge(status):
    from netbox_lifecycle.constants import CONTRACT_STATUS_COLOR

    if not status or status not in CONTRACT_STATUS_COLOR:
        return ''
    label, color = CONTRACT_STATUS_COLOR[status]
    return mark_safe(f'<span class="badge text-bg-{color}">{label}</span>')
