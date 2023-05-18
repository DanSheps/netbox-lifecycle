import django_filters
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils.translation import gettext as _

from dcim.models import Manufacturer, Device
from netbox.filtersets import NetBoxModelFilterSet
from netbox_lifecycle.models import Vendor, SupportContract, SupportContractAssignment, SupportSKU, LicenseAssignment

__all__ = (
    'SupportContractFilterSet',
    'SupportSKUFilterSet',
    'VendorFilterSet',
    'SupportContractAssignmentFilterSet'
)

from utilities.filters import MultiValueCharFilter, MultiValueNumberFilter


class VendorFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = Vendor
        fields = ('id', 'q', )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()


class SupportSKUFilterSet(NetBoxModelFilterSet):
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

    class Meta:
        model = SupportSKU
        fields = ('id', 'q', )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(sku__icontains=value) |
            Q(manufacturer__name__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()



class SupportContractFilterSet(NetBoxModelFilterSet):
    vendor_id = django_filters.ModelMultipleChoiceFilter(
        field_name='vendor',
        queryset=Vendor.objects.all(),
        label=_('Vendor'),
    )

    class Meta:
        model = SupportContract
        fields = ('id', 'q', )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(vendor__name__icontains=value) |
            Q(contract_id__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()


class SupportContractAssignmentFilterSet(NetBoxModelFilterSet):
    contract_id = django_filters.ModelMultipleChoiceFilter(
        field_name='contract',
        queryset=SupportContract.objects.all(),
        label=_('Contract'),
    )
    assigned_object_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ContentType.objects.all()
    )
    device = MultiValueCharFilter(
        method='filter_device',
        field_name='name',
        label=_('Device (name)'),
    )
    device_id = MultiValueNumberFilter(
        method='filter_device',
        field_name='pk',
        label=_('Device (ID)'),
    )
    license = MultiValueCharFilter(
        method='filter_license',
        field_name='name',
        label=_('License (SKU)'),
    )
    license_id = MultiValueNumberFilter(
        method='filter_license',
        field_name='pk',
        label=_('License (ID)'),
    )

    class Meta:
        model = SupportContractAssignment
        fields = ('id', 'q', )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(contract__contract_id__icontains=value) |
            Q(contract__vendor__name__icontains=value) |
            Q(sku__sku__icontains=value) |
            Q(device__name__icontains=value) |
            Q(license__device__name__icontains=value) |
            Q(license__license__name__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()

    def filter_device(self, queryset, name, value):
        licenses = LicenseAssignment.objects.filter(**{'device__{}__in'.format(name): value})
        devices = Device.objects.filter(**{'{}__in'.format(name): value})
        device_ids = devices.values_list('id', flat=True)
        license_ids = licenses.values_list('id', flat=True)

        return queryset.filter(
            Q(device__in=device_ids) | Q(license__in=license_ids)
        )

    def filter_license(self, queryset, name, value):
        return queryset.filter(
            license__in=value
        )
