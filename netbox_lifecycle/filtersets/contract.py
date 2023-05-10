import django_filters
from django.utils.translation import gettext as _

from dcim.models import Manufacturer, Device
from netbox.filtersets import NetBoxModelFilterSet
from netbox_lifecycle.models import Vendor, SupportContract


__all__ = (
    'SupportContractFilterSet',
    'VendorFilterSet'
)


class VendorFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = Vendor
        fields = ('id', 'q', )


class SupportContractFilterSet(NetBoxModelFilterSet):
    manufacturer_id = django_filters.ModelMultipleChoiceFilter(
        field_name='manufacturer',
        queryset=Manufacturer.objects.all(),
        label=_('Manufacturer'),
    )
    manufacturer = django_filters.ModelMultipleChoiceFilter(
        field_name='manufacturer__slug',
        queryset=Manufacturer.objects.all(),
        to_field_name='slug',
        label=_('Manufacturer (slug)'),
    )
    vendor_id = django_filters.ModelMultipleChoiceFilter(
        field_name='vendor',
        queryset=Vendor.objects.all(),
        label=_('Vendor'),
    )
    device_id = django_filters.ModelMultipleChoiceFilter(
        field_name='devices',
        queryset=Device.objects.all(),
        label=_('Device'),
    )

    class Meta:
        model = SupportContract
        fields = ('id', 'q', )
