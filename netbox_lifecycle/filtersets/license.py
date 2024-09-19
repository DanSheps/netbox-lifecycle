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
    manufacturer = django_filters.ModelMultipleChoiceFilter(
        field_name='manufacturer__slug',
        queryset=Manufacturer.objects.all(),
        to_field_name='slug',
        label=_('Manufacturer (Slug)'),
    )

    class Meta:
        model = License
        fields = ('id', 'q', 'name', )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(manufacturer__name__icontains=value) |
            Q(name__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()


class LicenseAssignmentFilterSet(NetBoxModelFilterSet):
    license_id = django_filters.ModelMultipleChoiceFilter(
        field_name='license',
        queryset=License.objects.all(),
        label=_('License'),
    )
    license = django_filters.ModelMultipleChoiceFilter(
        field_name='license__name',
        queryset=License.objects.all(),
        to_field_name='name',
        label=_('License'),
    )
    vendor_id = django_filters.ModelMultipleChoiceFilter(
        field_name='vendor',
        queryset=Vendor.objects.all(),
        label=_('Vendor'),
    )
    vendor = django_filters.ModelMultipleChoiceFilter(
        field_name='vendor__name',
        queryset=Vendor.objects.all(),
        to_field_name='name',
        label=_('Vendor'),
    )
    device_id = django_filters.ModelMultipleChoiceFilter(
        field_name='device',
        queryset=Device.objects.all(),
        label=_('Device'),
    )
    device = django_filters.ModelMultipleChoiceFilter(
        field_name='device__name',
        queryset=Device.objects.all(),
        to_field_name='name',
        label=_('Device'),
    )

    class Meta:
        model = LicenseAssignment
        fields = ('id', 'q', )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(license__manufacturer__name__icontains=value) |
            Q(license__name__icontains=value) |
            Q(vendor__name__icontains=value) |
            Q(device__name__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()
