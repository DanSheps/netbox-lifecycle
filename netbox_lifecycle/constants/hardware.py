from django.db.models import Q

__all__ = (
    'HARDWARE_LIFECYCLE_MODELS',
)

HARDWARE_LIFECYCLE_MODELS = Q(app_label='dcim', model__in=('moduletype', 'devicetype',))
