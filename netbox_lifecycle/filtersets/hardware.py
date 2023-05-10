import django_filters
from django.contrib.contenttypes.models import ContentType

from netbox.filtersets import NetBoxModelFilterSet
from netbox_lifecycle.models import HardwareLifecycle


__all__ = (
    'HardwareLifecycleFilterSet',
)


class HardwareLifecycleFilterSet(NetBoxModelFilterSet):
    assigned_object_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ContentType.objects.all()
    )

    class Meta:
        model = HardwareLifecycle
        fields = ('id', 'assigned_object_type_id', 'assigned_object_id', )
