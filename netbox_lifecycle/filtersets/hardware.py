import django_filters
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _
from django.db.models import Q

from dcim.models import ModuleType, DeviceType
from netbox.filtersets import NetBoxModelFilterSet
from netbox_lifecycle.models import HardwareLifecycle


__all__ = (
    'HardwareLifecycleFilterSet',
)


class HardwareLifecycleFilterSet(NetBoxModelFilterSet):
    assigned_object_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ContentType.objects.all()
    )
    device_type = django_filters.ModelMultipleChoiceFilter(
        field_name='device_type__model',
        queryset=DeviceType.objects.all(),
        to_field_name='model',
        label=_('Device Type (Model)'),
    )
    device_type_id = django_filters.ModelMultipleChoiceFilter(
        field_name='device_type',
        queryset=DeviceType.objects.all(),
        label=_('Device Type'),
    )
    module_type = django_filters.ModelMultipleChoiceFilter(
        field_name='module_type__model',
        queryset=ModuleType.objects.all(),
        to_field_name='model',
        label=_('Module Type (Model)'),
    )
    module_type_id = django_filters.ModelMultipleChoiceFilter(
        field_name='module_type',
        queryset=ModuleType.objects.all(),
        label=_('Module Type'),
    )

    class Meta:
        model = HardwareLifecycle
        fields = (
            'id', 'assigned_object_type_id', 'assigned_object_id',
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(device_type__model__icontains=value) |
            Q(module_type__model__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()
