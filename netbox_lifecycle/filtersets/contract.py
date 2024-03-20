import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _

from dcim.models import Manufacturer, Device
from netbox.filtersets import NetBoxModelFilterSet
from netbox_lifecycle.models import Vendor, SupportContract, SupportContractAssignment, SupportSKU, LicenseAssignment, \
    License

__all__ = (
    'SupportContractFilterSet',
    'SupportSKUFilterSet',
    'VendorFilterSet',
    'SupportContractAssignmentFilterSet'
)


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
    device = django_filters.ModelMultipleChoiceFilter(
        field_name='device__name',
        queryset=Device.objects.all(),
        label=_('Device (name)'),
    )
    device_id = django_filters.ModelMultipleChoiceFilter(
        field_name='device',
        queryset=Device.objects.all(),
        label=_('Device (ID)'),
    )
    license = django_filters.ModelMultipleChoiceFilter(
        field_name='license__license__name',
        queryset=License.objects.all(),
        label=_('License (SKU)'),
    )
    license_id = django_filters.ModelMultipleChoiceFilter(
        field_name='license',
        queryset=LicenseAssignment.objects.all(),
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
