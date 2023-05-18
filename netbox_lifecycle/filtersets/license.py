import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _

from dcim.models import Manufacturer, Device
from netbox.filtersets import NetBoxModelFilterSet
from netbox_lifecycle.models import Vendor, License, LicenseAssignment

__all__ = (
    'LicenseFilterSet',
    'LicenseAssignmentFilterSet',
)


class LicenseFilterSet(NetBoxModelFilterSet):
    manufacturer_id = django_filters.ModelMultipleChoiceFilter(
        field_name='manufacturer',
        queryset=Manufacturer.objects.all(),
        label=_('Manufacturer'),
    )

    class Meta:
        model = License
        fields = ('id', 'q', )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(manufacturer__name_icontains=value) |
            Q(name__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()


class LicenseAssignmentFilterSet(NetBoxModelFilterSet):
    license_id = django_filters.ModelMultipleChoiceFilter(
        field_name='license',
        queryset=License.objects.all(),
        label=_('License'),
    )
    vendor_id = django_filters.ModelMultipleChoiceFilter(
        field_name='license',
        queryset=Vendor.objects.all(),
        label=_('Vendor'),
    )
    device_id = django_filters.ModelMultipleChoiceFilter(
        field_name='license',
        queryset=Device.objects.all(),
        label=_('Device'),
    )

    class Meta:
        model = LicenseAssignment
        fields = ('id', 'q', )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(license__manufacturer__name_icontains=value) |
            Q(license__name__icontains=value) |
            Q(vendor__name__icontains=value) |
            Q(device__name__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()
