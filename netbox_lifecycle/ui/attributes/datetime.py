import datetime

from django.utils.safestring import mark_safe

from netbox.ui.attrs import DateTimeAttr

__all__ = ('ColoredDateTimeAttr',)


class ColoredDateTimeAttr(DateTimeAttr):
    """
    A DateTimeAttr that applies a badge to the value when rendered.
    """

    def get_class(self, value):
        if datetime.datetime.now(tz=datetime.timezone.utc).date() > value:
            return 'text-bg-danger'
        elif (
            datetime.datetime.now(tz=datetime.timezone.utc).date()
            + datetime.timedelta(days=183)
            > value
        ):
            return 'text-bg-warning'
        else:
            return 'badge-neutral'
        return ''

    def render(self, obj, context):
        value = self.get_value(obj)
        rendered = super().render(obj, context)
        if value:
            rendered = mark_safe(
                f'<span class="badge {self.get_class(value)}">{rendered}</span>'
            )
        return rendered
