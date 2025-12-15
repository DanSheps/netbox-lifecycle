from django import forms
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.forms import DateField

from dcim.choices import DeviceStatusChoices
from dcim.models import Device, Manufacturer, Module
from netbox.forms import NetBoxModelFilterSetForm
from virtualization.models import VirtualMachine
from netbox_lifecycle.models import (
    HardwareLifecycle,
    SupportContract,
    Vendor,
    License,
    LicenseAssignment,
    SupportContractAssignment,
    SupportSKU,
)
from utilities.forms.fields import (
    DynamicModelMultipleChoiceField,
    TagFilterField,
)
from utilities.forms.rendering import FieldSet
from utilities.forms.widgets import APISelectMultiple, DatePicker


__all__ = (
    'HardwareLifecycleFilterForm',
    'SupportSKUFilterForm',
    'SupportContractFilterForm',
    'VendorFilterForm',
    'LicenseFilterForm',
    'LicenseAssignmentFilterForm',
    'SupportContractAssignmentFilterForm',
)


class HardwareLifecycleFilterForm(NetBoxModelFilterSetForm):
    model = HardwareLifecycle
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet('assigned_object_type_id', name=_('Hardware')),
        FieldSet(
            'end_of_sale__lt',
            'end_of_maintenance__lt',
            'end_of_security__lt',
            'end_of_support__lt',
            name=_('Dates'),
        ),
    )

    assigned_object_type_id = DynamicModelMultipleChoiceField(
        queryset=ContentType.objects.filter(
            Q(app_label='dcim', model='devicetype')
            | Q(app_label='dcim', model='moduletype')
        ),
        required=False,
        label=_('Object Type'),
        widget=APISelectMultiple(
            api_url='/api/extras/content-types/',
        ),
    )
    end_of_sale__lt = DateField(
        required=False,
        label=_('End of sale before'),
        widget=DatePicker,
    )
    end_of_maintenance__lt = DateField(
        required=False,
        label=_('End of maintenance before'),
    )
    end_of_security__lt = DateField(
        required=False,
        label=_('End of security before'),
        widget=DatePicker,
    )
    end_of_support__lt = DateField(
        required=False,
        label=_('End of support before'),
        widget=DatePicker,
    )
    tag = TagFilterField(model)


class SupportSKUFilterForm(NetBoxModelFilterSetForm):
    model = SupportSKU
    fieldsets = (FieldSet('q', 'filter_id', 'tag', 'manufacturer_id'),)
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
    fieldsets = (FieldSet('q', 'filter_id', 'tag'),)
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
        FieldSet(
            'contract_id',
            'device_id',
            'module_id',
            'virtual_machine_id',
            'license_id',
            'device_status',
            name='Assignment',
        ),
    )
    contract_id = DynamicModelMultipleChoiceField(
        queryset=SupportContract.objects.all(),
        required=False,
        selector=True,
        label=_('Support Contracts'),
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
    module_id = DynamicModelMultipleChoiceField(
        queryset=Module.objects.all(),
        required=False,
        label=_('Module'),
    )
    virtual_machine_id = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        selector=True,
        label=_('Virtual Machines'),
    )
    device_status = forms.MultipleChoiceField(
        label=_('Status'), choices=DeviceStatusChoices, required=False
    )
    tag = TagFilterField(model)


class LicenseAssignmentFilterForm(NetBoxModelFilterSetForm):
    model = LicenseAssignment
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet(
            'license_id',
            'vendor_id',
            'device_id',
            'virtual_machine_id',
            name='Assignment',
        ),
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
    virtual_machine_id = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        selector=True,
        label=_('Virtual Machines'),
    )
    tag = TagFilterField(model)
