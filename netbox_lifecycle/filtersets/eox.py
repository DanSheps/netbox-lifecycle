import django_filters
from dcim.models import Manufacturer
from django.db.models import Q
from django.utils.translation import gettext as _
from netbox.filtersets import NetBoxModelFilterSet
from utilities.filtersets import register_filterset

from netbox_lifecycle.choices.eox import DriverChoices
from netbox_lifecycle.models import EoXAPISettings

__all__ = ('EoXAPISettingsFilterSet',)


@register_filterset
class EoXAPISettingsFilterSet(NetBoxModelFilterSet):
    driver = django_filters.MultipleChoiceFilter(
        choices=DriverChoices,
        label=_('Driver'),
    )
    manufacturer_id = django_filters.ModelMultipleChoiceFilter(
        field_name='manufacturer',
        queryset=Manufacturer.objects.all(),
        label=_('Manufacturer'),
    )
    manufacturer = django_filters.ModelMultipleChoiceFilter(
        field_name='manufacturer__name',
        queryset=Manufacturer.objects.all(),
        to_field_name='name',
        label=_('Manufacturer (name)'),
    )

    class Meta:
        model = EoXAPISettings
        fields = (
            'id',
            'q',
            'driver',
            'enabled',
            'manufacturer_id',
            'sync_interval',
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(client_id__icontains=value) | Q(description__icontains=value)
        return queryset.filter(qs_filter).distinct()
