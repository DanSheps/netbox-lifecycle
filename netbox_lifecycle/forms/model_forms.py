from django import forms
from django.utils.translation import gettext as _

from dcim.models import DeviceType, ModuleType, Manufacturer, Device, Module
from netbox.forms import NetBoxModelForm
from netbox_lifecycle.models import (
    HardwareLifecycle,
    Vendor,
    SupportContract,
    LicenseAssignment,
    License,
    SupportContractAssignment,
    SupportSKU,
)
from utilities.forms.fields import (
    DynamicModelChoiceField,
)
from utilities.forms.rendering import FieldSet, TabbedGroups
from utilities.forms.widgets import DatePicker


__all__ = (
    'VendorForm',
    'SupportSKUForm',
    'SupportContractForm',
    'SupportContractAssignmentForm',
    'LicenseForm',
    'LicenseAssignmentForm',
    'HardwareLifecycleForm',
)


class VendorForm(NetBoxModelForm):

    class Meta:
        model = Vendor
        fields = (
            'name',
            'description',
            'comments',
            'tags',
        )


class SupportSKUForm(NetBoxModelForm):
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        selector=False,
    )

    class Meta:
        model = SupportSKU
        fields = (
            'manufacturer',
            'sku',
            'description',
            'comments',
            'tags',
        )


class SupportContractForm(NetBoxModelForm):
    vendor = DynamicModelChoiceField(
        queryset=Vendor.objects.all(),
        selector=True,
    )

    class Meta:
        model = SupportContract
        fields = (
            'vendor',
            'contract_id',
            'start',
            'renewal',
            'end',
            'description',
            'comments',
            'tags',
        )
        widgets = {
            'start': DatePicker(),
            'renewal': DatePicker(),
            'end': DatePicker(),
        }


class SupportContractAssignmentForm(NetBoxModelForm):
    contract = DynamicModelChoiceField(
        queryset=SupportContract.objects.all(),
        selector=True,
    )
    sku = DynamicModelChoiceField(
        queryset=SupportSKU.objects.all(),
        required=False,
        selector=True,
        label=_('SKU'),
    )
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('Device'),
    )
    module = DynamicModelChoiceField(
        queryset=Module.objects.all(),
        required=False,
        selector=True,
        label=_('Module'),
        query_params={'device_id': '$device'},
    )
    license = DynamicModelChoiceField(
        queryset=LicenseAssignment.objects.all(),
        required=False,
        selector=True,
        label=_('License Assignment'),
    )

    fieldsets = (
        FieldSet('contract', 'sku', name=_('Contract')),
        FieldSet(
            TabbedGroups(
                FieldSet('device', 'module', name=_('Hardware')),
                FieldSet('license', name=_('License')),
            ),
            name=_('Assignment'),
        ),
        FieldSet('end', name=_('Dates')),
        FieldSet('description', 'comments', 'tags', name=_('Other')),
    )

    class Meta:
        model = SupportContractAssignment
        fields = (
            'contract',
            'sku',
            'device',
            'module',
            'license',
            'end',
            'description',
            'comments',
            'tags',
        )
        widgets = {
            'end': DatePicker(),
        }

    def clean(self):
        super().clean()

        has_hardware = self.cleaned_data.get('device') or self.cleaned_data.get(
            'module'
        )
        has_license = self.cleaned_data.get('license')

        # Must select at least one assignment target
        if not has_hardware and not has_license:
            raise forms.ValidationError(
                _('Select a device, module, or license assignment')
            )

        # Auto-populate device from module if module selected without device
        if self.cleaned_data.get('module') and not self.cleaned_data.get('device'):
            self.cleaned_data['device'] = self.cleaned_data['module'].device

        # Validate device matches module.device
        if (
            self.cleaned_data.get('device')
            and self.cleaned_data.get('module')
            and self.cleaned_data['device'] != self.cleaned_data['module'].device
        ):
            raise forms.ValidationError(
                {'module': _('Module must belong to the selected device')}
            )

        # Auto-populate device from license if license selected without device
        if self.cleaned_data.get('license') and not self.cleaned_data.get('device'):
            self.cleaned_data['device'] = self.cleaned_data['license'].device

        # Validate device matches license.device if both are set
        if (
            self.cleaned_data.get('license')
            and self.cleaned_data.get('device')
            and self.cleaned_data['license'].device
            and self.cleaned_data['device'] != self.cleaned_data['license'].device
        ):
            raise forms.ValidationError(
                {'device': _('Device must match the device assigned to the license')}
            )

        return self.cleaned_data


class LicenseForm(NetBoxModelForm):
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        selector=False,
    )

    class Meta:
        model = License
        fields = (
            'manufacturer',
            'name',
            'description',
            'comments',
            'tags',
        )


class LicenseAssignmentForm(NetBoxModelForm):
    vendor = DynamicModelChoiceField(
        queryset=Vendor.objects.all(),
        selector=True,
    )
    license = DynamicModelChoiceField(
        queryset=License.objects.all(),
        selector=True,
    )
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
    )

    class Meta:
        model = LicenseAssignment
        fields = (
            'vendor',
            'license',
            'device',
            'quantity',
            'description',
            'comments',
            'tags',
        )


class HardwareLifecycleForm(NetBoxModelForm):
    device_type = DynamicModelChoiceField(
        queryset=DeviceType.objects.all(),
        required=False,
        selector=True,
        label=_('Device Type'),
    )
    module_type = DynamicModelChoiceField(
        queryset=ModuleType.objects.all(),
        required=False,
        selector=True,
        label=_('Module Type'),
    )

    fieldsets = (
        FieldSet(
            TabbedGroups(
                FieldSet('device_type', name=_('Device Type')),
                FieldSet('module_type', name=_('Module Type')),
            ),
        ),
        FieldSet(
            'last_contract_attach',
            'last_contract_renewal',
            'end_of_sale',
            'end_of_maintenance',
            'end_of_security',
            'end_of_support',
            name=_('Dates'),
        ),
        FieldSet('notice', 'documentation', 'description', name=_('Information')),
        FieldSet('tags', name=_('Tags')),
    )

    class Meta:
        model = HardwareLifecycle
        fields = (
            'last_contract_attach',
            'last_contract_renewal',
            'end_of_sale',
            'end_of_maintenance',
            'end_of_security',
            'end_of_support',
            'notice',
            'documentation',
            'description',
            'comments',
            'tags',
        )
        widgets = {
            'last_contract_attach': DatePicker(),
            'last_contract_renewal': DatePicker(),
            'end_of_sale': DatePicker(),
            'end_of_maintenance': DatePicker(),
            'end_of_security': DatePicker(),
            'end_of_support': DatePicker(),
        }

    def __init__(self, *args, **kwargs):
        # Initialize helper selectors
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {}).copy()
        if instance:
            if type(instance.assigned_object) is DeviceType:
                initial['device_type'] = instance.assigned_object
            elif type(instance.assigned_object) is ModuleType:
                initial['module_type'] = instance.assigned_object
        kwargs['initial'] = initial

        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        # Handle object assignment
        selected_objects = [
            field
            for field in ('device_type', 'module_type')
            if self.cleaned_data[field]
        ]

        if len(selected_objects) > 1:
            raise forms.ValidationError(
                {
                    selected_objects[
                        1
                    ]: "You can only have a lifecycle for a device or module type"
                }
            )
        elif selected_objects:
            self.instance.assigned_object = self.cleaned_data[selected_objects[0]]
        else:
            self.instance.assigned_object = None
