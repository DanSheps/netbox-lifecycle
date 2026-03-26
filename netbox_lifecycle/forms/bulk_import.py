from dcim.models import Device, DeviceType, Manufacturer, Module, ModuleType
from django.utils.translation import gettext_lazy as _
from netbox.forms import NetBoxModelImportForm
from utilities.forms.fields import CSVModelChoiceField
from virtualization.models import VirtualMachine

from netbox_lifecycle.models import (
    HardwareLifecycle,
    License,
    LicenseAssignment,
    SupportContract,
    SupportContractAssignment,
    SupportSKU,
    Vendor,
)

__all__ = (
    'HardwareLifecycleImportForm',
    'LicenseAssignmentImportForm',
    'LicenseImportForm',
    'SupportContractAssignmentImportForm',
    'SupportContractImportForm',
    'SupportSKUImportForm',
    'VendorImportForm',
)


class VendorImportForm(NetBoxModelImportForm):
    class Meta:
        model = Vendor
        fields = ('name', 'description', 'comments', 'tags')


class SupportSKUImportForm(NetBoxModelImportForm):
    manufacturer = CSVModelChoiceField(
        label=_('Manufacturer'),
        queryset=Manufacturer.objects.all(),
        to_field_name='name',
        help_text=_('Manufacturer name'),
    )

    class Meta:
        model = SupportSKU
        fields = ('manufacturer', 'sku', 'description', 'comments', 'tags')


class SupportContractImportForm(NetBoxModelImportForm):
    vendor = CSVModelChoiceField(
        label=_('Vendor'),
        queryset=Vendor.objects.all(),
        to_field_name='name',
        help_text=_('Vendor name'),
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


class SupportContractAssignmentImportForm(NetBoxModelImportForm):
    contract = CSVModelChoiceField(
        label=_('Contract'),
        queryset=SupportContract.objects.all(),
        to_field_name='contract_id',
        help_text=_('Contract ID'),
    )
    sku = CSVModelChoiceField(
        label=_('SKU'),
        queryset=SupportSKU.objects.all(),
        required=False,
        to_field_name='sku',
        help_text=_('Support SKU'),
    )
    device = CSVModelChoiceField(
        label=_('Device'),
        queryset=Device.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Device name'),
    )
    module = CSVModelChoiceField(
        label=_('Module'),
        queryset=Module.objects.all(),
        required=False,
        to_field_name='id',
        help_text=_('Module ID'),
    )
    virtual_machine = CSVModelChoiceField(
        label=_('Virtual Machine'),
        queryset=VirtualMachine.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Virtual machine name'),
    )
    license = CSVModelChoiceField(
        label=_('License Assignment'),
        queryset=LicenseAssignment.objects.all(),
        required=False,
        to_field_name='id',
        help_text=_('License assignment ID'),
    )

    class Meta:
        model = SupportContractAssignment
        fields = (
            'contract',
            'sku',
            'device',
            'module',
            'virtual_machine',
            'license',
            'end',
            'description',
            'comments',
            'tags',
        )


class LicenseImportForm(NetBoxModelImportForm):
    manufacturer = CSVModelChoiceField(
        label=_('Manufacturer'),
        queryset=Manufacturer.objects.all(),
        to_field_name='name',
        help_text=_('Manufacturer name'),
    )

    class Meta:
        model = License
        fields = ('manufacturer', 'name', 'description', 'comments', 'tags')


class LicenseAssignmentImportForm(NetBoxModelImportForm):
    license = CSVModelChoiceField(
        label=_('License'),
        queryset=License.objects.all(),
        to_field_name='name',
        help_text=_('License name'),
    )
    vendor = CSVModelChoiceField(
        label=_('Vendor'),
        queryset=Vendor.objects.all(),
        to_field_name='name',
        help_text=_('Vendor name'),
    )
    device = CSVModelChoiceField(
        label=_('Device'),
        queryset=Device.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Device name'),
    )
    virtual_machine = CSVModelChoiceField(
        label=_('Virtual Machine'),
        queryset=VirtualMachine.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Virtual machine name'),
    )

    class Meta:
        model = LicenseAssignment
        fields = (
            'license',
            'vendor',
            'device',
            'virtual_machine',
            'quantity',
            'description',
            'comments',
            'tags',
        )


class HardwareLifecycleImportForm(NetBoxModelImportForm):
    device_type = CSVModelChoiceField(
        label=_('Device Type'),
        queryset=DeviceType.objects.all(),
        required=False,
        to_field_name='model',
        help_text=_('Device type model name'),
    )
    module_type = CSVModelChoiceField(
        label=_('Module Type'),
        queryset=ModuleType.objects.all(),
        required=False,
        to_field_name='model',
        help_text=_('Module type model name'),
    )

    class Meta:
        model = HardwareLifecycle
        fields = (
            'device_type',
            'module_type',
            'end_of_sale',
            'end_of_maintenance',
            'end_of_security',
            'last_contract_attach',
            'last_contract_renewal',
            'end_of_support',
            'notice',
            'documentation',
            'description',
            'comments',
            'tags',
        )

    def clean(self):
        super().clean()

        device_type = self.cleaned_data.get('device_type')
        module_type = self.cleaned_data.get('module_type')

        # Validate mutual exclusivity
        if device_type and module_type:
            raise ValueError(
                _('Cannot specify both device_type and module_type. Choose one.')
            )

        if not device_type and not module_type:
            raise ValueError(_('Must specify either device_type or module_type.'))

        return self.cleaned_data

    def save(self, *args, **kwargs):
        # Set the assigned_object based on device_type or module_type
        device_type = self.cleaned_data.get('device_type')
        module_type = self.cleaned_data.get('module_type')

        if device_type:
            self.instance.assigned_object = device_type
        elif module_type:
            self.instance.assigned_object = module_type

        return super().save(*args, **kwargs)
