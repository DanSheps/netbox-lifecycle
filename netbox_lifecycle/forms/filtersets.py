from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from dcim.models import Device, Manufacturer
from netbox.forms import NetBoxModelFilterSetForm
from netbox_lifecycle.models import HardwareLifecycle, SupportContract, Vendor, License, LicenseAssignment, \
    SupportContractAssignment, SupportSKU
from utilities.filters import MultiValueCharFilter, MultiValueNumberFilter
from utilities.forms.fields import DynamicModelMultipleChoiceField, TagFilterField
from utilities.forms.rendering import FieldSet
from utilities.forms.widgets import APISelectMultiple


__all__ = (
    'HardwareLifecycleFilterForm',
    'SupportSKUFilterForm',
    'SupportContractFilterForm',
    'VendorFilterForm',
    'LicenseFilterForm',
    'LicenseAssignmentFilterForm',
    'SupportContractAssignmentFilterForm'
)


class HardwareLifecycleFilterForm(NetBoxModelFilterSetForm):
    model = HardwareLifecycle
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet('assigned_object_type_id', name=_('Hardware'))
    )

    assigned_object_type_id = DynamicModelMultipleChoiceField(
        queryset=ContentType.objects.filter(Q(app_label='dcim', model='devicetype') | Q(app_label='dcim', model='moduletype')),
        required=False,
        label=_('Object Type'),
        widget=APISelectMultiple(
            api_url='/api/extras/content-types/',
        )
    )
    tag = TagFilterField(model)


class SupportSKUFilterForm(NetBoxModelFilterSetForm):
    model = SupportSKU
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag', 'manufacturer_id'),
    )
    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        selector=True,
        label=_('Manufacturer'),
    )
    tag = TagFilterField(model)


class SupportContractFilterForm(NetBoxModelFilterSetForm):
    model = SupportContract
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet('vendor_id', name='Purchase Information'),
    )
    vendor_id = DynamicModelMultipleChoiceField(
        queryset=Vendor.objects.all(),
        required=False,
        selector=True,
        label=_('Vendor'),
    )
    tag = TagFilterField(model)


class VendorFilterForm(NetBoxModelFilterSetForm):
    model = Vendor
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
    )
    tag = TagFilterField(model)


class LicenseFilterForm(NetBoxModelFilterSetForm):
    model = License
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet('manufacturer_id', name='License Information'),
    )
    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        selector=True,
        label=_('Manufacturer'),
    )
    tag = TagFilterField(model)


class SupportContractAssignmentFilterForm(NetBoxModelFilterSetForm):
    model = SupportContractAssignment
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet('contract_id', 'device_id', 'license_id', name='Assignment'),
    )
    contract_id = DynamicModelMultipleChoiceField(
        queryset=SupportContract.objects.all(),
        required=False,
        selector=True,
        label=_('Contracts'),
    )
    license_id = DynamicModelMultipleChoiceField(
        queryset=License.objects.all(),
        required=False,
        selector=True,
        label=_('Licenses'),
    )
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('Devices'),
    )
    tag = TagFilterField(model)


class LicenseAssignmentFilterForm(NetBoxModelFilterSetForm):
    model = LicenseAssignment
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet('license_id', 'vendor_id', 'device_id', name='Assignment'),
    )
    license_id = DynamicModelMultipleChoiceField(
        queryset=License.objects.all(),
        required=False,
        selector=True,
        label=_('Licenses'),
    )
    vendor_id = DynamicModelMultipleChoiceField(
        queryset=Vendor.objects.all(),
        required=False,
        selector=True,
        label=_('Vendors'),
    )
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('Devices'),
    )
    tag = TagFilterField(model)
