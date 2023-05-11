import django_filters
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _

from dcim.models import Manufacturer, Device
from netbox.filtersets import NetBoxModelFilterSet
from netbox_lifecycle.models import Vendor, SupportContract, SupportContractAssignment

__all__ = (
    'SupportContractFilterSet',
    'VendorFilterSet',
    'SupportContractAssignmentFilterSet'
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

    class Meta:
        model = SupportContract
        fields = ('id', 'q', )


class SupportContractAssignmentFilterSet(NetBoxModelFilterSet):
    contract_id = django_filters.ModelMultipleChoiceFilter(
        field_name='contract',
        queryset=SupportContract.objects.all(),
        label=_('Contract'),
    )
    assigned_object_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ContentType.objects.all()
    )

    class Meta:
        model = SupportContractAssignment
        fields = ('id', 'q', 'assigned_object_type_id', 'assigned_object_id', )
